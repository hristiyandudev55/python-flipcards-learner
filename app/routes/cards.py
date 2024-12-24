from typing import Literal
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import CardEdit, FlipCardCreate, FlipCardResponse
from crud import (
    create_card,
    delete_card,
    edit_card,
    get_all_cards,
    get_all_cards_from_category,
)
from database import get_db


CategoryType = Literal["OOP", "DSA", "WEB", "AZURE", "LINUX", "DOCKER", "KUBERNETES", "CI_CD", "GENERAL"]
cards_router = APIRouter(prefix="/api/cards", tags=["Cards"])


@cards_router.post("/", response_model=FlipCardResponse)
def create_card_route(card_data: FlipCardCreate, db: Session = Depends(get_db)):
    """
    This route creates a new flashcard based on the provided data.

    Args:
        card_data: The data used to create the card.
        db (Session): Database session.

    Returns:
        FlipCardResponse: The created card.
    """
    return create_card(db=db, card_data=card_data)


@cards_router.get("/{category}", response_model=list[FlipCardResponse])
def read_cards_from_category(category: CategoryType, db: Session = Depends(get_db)):
    """
    Route for retrieving all cards from a specific category.

    Args:
        category (CategoryType): The category to filter cards by (OOP, DSA, WEB).
        db (Session): The database session provided by dependency injection.

    Raises:
        HTTPException: If no cards are found in the specified category.

    Returns:
        list[FlipCardResponse]: A list of cards in the specified category.
    """
    try:
        return get_all_cards_from_category(db=db, category=category)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e


@cards_router.get("/", response_model=list[FlipCardResponse])
def read_all_cards(db: Session = Depends(get_db)):
    """
    Route for retrieving all cards.

    Args:
    db (Session): The database session.

    Raises:
        HTTPException: If no cards are found.

    Returns:
        list[FlipCardResponse]: A list of all cards.
    """
    try:
        return get_all_cards(db=db)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=e.detail) from e


@cards_router.patch("/{card_id}", response_model=FlipCardResponse)
def edit_flip_card(card_id: int, card_data: CardEdit, db: Session = Depends(get_db)):
    """
    This route edits a card based on the provided card_id and card_data.

    Args:
        card_id: The id of the card to edit.
        card_data: The data used to edit the card.
        db (Session): Database session.

    Returns:
        FlipCardResponse: The edited card.

    Raises:
        HTTPException: If the card is not found.
    """
    try:
        return edit_card(db=db, card_data=card_data, card_id=card_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=e.detail) from e


@cards_router.delete("/{card_id}")
def delete_flip_card(card_id: int, db: Session = Depends(get_db)):
    """
    This route deletes a card based on the provided card_id.

    Args:
        card_id: The id of the card to delete.
        db (Session): Database session.

    Raises:
        HTTPException: If the card is not found.
    """
    try:
        return delete_card(card_id=card_id, db=db)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=e.detail) from e
