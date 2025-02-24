from typing import Literal

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.enums import Categories
from app.models import FlipCard
from app.schemas import CardEdit, FlipCardCreate, FlipCardResponse


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
            raise HTTPException(status_code=400, detail="This card already exists!")

        card = FlipCard(
            front_text=card_data.front_text,
            back_text=card_data.back_text,
            category=card_data.category,
        )

        db.add(card)
        db.commit()
        db.refresh(card)

        return FlipCardResponse.model_validate(card)

    except SQLAlchemyError as e:
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


CategoryLiteral = Literal["OOP", "DSA", "WEB", "DOCKER", "KUBERNETES", "LINUX", "AZURE", "CI_CD"]


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
        raise HTTPException(
            status_code=404,
            detail=f"Card with ID {card_id} not found. Please try a different ID.",
        )

    updated = False
    if card_data.front_text is not None:
        card.front_text = card_data.front_text
        updated = True
    if card_data.back_text is not None:
        card.back_text = card_data.back_text
        updated = True
    if card_data.category is not None:
        card.category = card_data.category
        updated = True

    if not updated:
        raise HTTPException(
            status_code=400, detail="No valid fields provided for update."
        )

    db.commit()
    db.refresh(card)

    return FlipCardResponse.model_validate(card)


def delete_card(db: Session, card_id: int) -> None:
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
        raise HTTPException(
            status_code=404, detail=f"Card with ID {card_id} not found!"
        )

    db.delete(card)
    db.commit()
