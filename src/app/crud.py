from typing import Literal

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.enums import Categories
from app.models import FlipCard
from app.schemas import CardEdit, FlipCardCreate, FlipCardResponse
from app.utils.s3_logger import s3_logger
from app.enums import LogAction


def create_card(db: Session, card_data: FlipCardCreate) -> FlipCardResponse:
    """
    This function creates a new card in the database.

    Args:
        db (Session): The database session used to interact with the database.
        card_data (FlipCardCreate): The data for the new card, including front and back text and category.

    Raises:
        HTTPException: If the category is not valid, if the card already exists in the database,
                       or if a database error occurs during creation.

    Returns:
        FlipCardResponse: The created card, validated and serialized into a response format.
    """
    try:
        if card_data.category not in Categories.__members__:
            error_msg = f"Category '{card_data.category}' is not a valid category!"
            s3_logger.log_action(
                LogAction.ERROR.value, {"error": error_msg, "operation": "create_card"}
            )
            raise HTTPException(
                status_code=400,
                detail=f"Category '{card_data.category}' is not a valid category!",
            )

        card_duplicate = (
            db.query(FlipCard)
            .filter(
                FlipCard.front_text == card_data.front_text,
                FlipCard.category == card_data.category,
            )
            .first()
        )
        if card_duplicate:
            error_msg = "This card already exists!"
            s3_logger.log_action(
                LogAction.ERROR.value, {"error": error_msg, "operation": "create_card"}
            )
            raise HTTPException(status_code=400, detail="This card already exists!")

        card = FlipCard(
            front_text=card_data.front_text,
            back_text=card_data.back_text,
            category=card_data.category,
        )

        db.add(card)
        db.commit()
        db.refresh(card)

        s3_logger.log_action(
            LogAction.CARD_CREATED.value,
            {
                "card_id": card.id,
                "category": card.category,
                "front_text": card.front_text,
            },
        )

        return FlipCardResponse.model_validate(card)

    except SQLAlchemyError as e:
        s3_logger.log_action(
            LogAction.ERROR.value, {"operation": "create_card", "error": str(e)}
        )
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the card: {str(e)}",
        ) from e


def get_all_cards(db: Session) -> list[FlipCardResponse]:
    """
    This function retrieves all cards from the database.

    Args:
        db (Session): The database session used to interact with the database.

    Returns:
        List[FlipCardResponse]: A list of all cards in the database, serialized into response format.
    """
    all_cards = db.query(FlipCard).all()

    return [FlipCardResponse.model_validate(card) for card in all_cards]


CategoryLiteral = Literal[
    "OOP", "DSA", "WEB", "DOCKER", "KUBERNETES", "LINUX", "AZURE", "CI_CD"
]


def get_all_cards_from_category(
    db: Session, category: CategoryLiteral
) -> list[FlipCardResponse]:
    """
    This function retrieves all cards from a specified category.

    Args:
        db (Session): The database session used to interact with the database.
        category (CategoryLiteral): The name of the category to filter the cards by.
                                    Allowed values: "OOP", "DSA", "WEB".

    Raises:
        HTTPException: If no cards are found in the specified category.

    Returns:
        List[FlipCardResponse]: A list of all cards from the specified category, serialized into response format.
    """
    cards_from_category = db.query(FlipCard).filter(FlipCard.category == category).all()

    if not cards_from_category:
        raise HTTPException(
            status_code=404, detail=f"No cards found in category {category}."
        )

    return [FlipCardResponse.model_validate(card) for card in cards_from_category]


def edit_card(db: Session, card_id: int, card_data: CardEdit) -> FlipCardResponse:
    """
    This function edits an existing card based on the provided card ID and new data.

    Args:
        db (Session): The database session used to interact with the database.
        card_id (int): The ID of the card to be updated.
        card_data (CardEdit): The new data to update the card with.

    Raises:
        HTTPException: If the card with the specified ID is not found or if no valid fields are provided for the update.

    Returns:
        FlipCardResponse: The updated card, serialized into response format.
    """
    card = db.query(FlipCard).filter(FlipCard.id == card_id).first()

    if not card:
        error_msg = f"Card with id {card_id} not found"
        s3_logger.log_action(
            LogAction.ERROR.value, {"error": error_msg, "operation": "update_card"}
        )
        raise HTTPException(
            status_code=404,
            detail=f"Card with ID {card_id} not found. Please try a different ID.",
        )

    updated = False
    if card_data.front_text is not None:
        card.front_text = card_data.front_text
        s3_logger.log_action(
            LogAction.CARD_UPDATED.value,
            {
                "card_id": card.id,
                "updated_field": "front_text",
                "front_text": card.front_text,
            },
        )
        updated = True
    if card_data.back_text is not None:
        card.back_text = card_data.back_text
        s3_logger.log_action(
            LogAction.CARD_UPDATED.value,
            {
                "card_id": card.id,
                "updated_field": "back_text",
                "new_value": card.back_text,
            },
        )
        updated = True
    if card_data.category is not None:
        card.category = card_data.category
        s3_logger.log_action(
            LogAction.CARD_UPDATED.value,
            {
                "card_id": card.id,
                "updated_field": "category",
                "new_value": card.category,
            },
        )
        updated = True

    if not updated:
        error_msg = "No valid fields provided for update"
        s3_logger.log_action(
            LogAction.ERROR.value, {"error": error_msg, "operation": "update_card"}
        )
        raise HTTPException(
            status_code=400, detail="No valid fields provided for update."
        )

    db.commit()
    db.refresh(card)

    return FlipCardResponse.model_validate(card)


def delete_card(db: Session, card_id: int):
    """
    This function deletes a card from the database based on the provided card ID.

    Args:
        db (Session): The database session used to interact with the database.
        card_id (int): The ID of the card to be deleted.

    Raises:
        HTTPException: If the card with the specified ID is not found.

    Returns:
        None: The function does not return anything. It either deletes the card or raises an exception if not found.
    """
    card = db.query(FlipCard).filter(FlipCard.id == card_id).first()

    if not card:
        error_msg = f"Card with id {card_id} not found"
        s3_logger.log_action(
            LogAction.ERROR.value, {"error": error_msg, "operation": "delete_card"}
        )
        raise HTTPException(
            status_code=404, detail=f"Card with ID {card_id} not found!"
        )

    db.delete(card)
    db.commit()

    s3_logger.log_action(
        LogAction.CARD_DELETED.value, {"card_id": card_id, "category": card.category}
    )
    return {"message": "Card deleted successfully"}
