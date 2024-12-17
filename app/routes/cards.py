from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import FlipCardCreate, FlipCardResponse
from crud import create_card
from database import get_db


cards_router = APIRouter(prefix="/api/cards", tags=["Cards"])


@cards_router.post("/", response_model=FlipCardResponse)
def create_card_route(
    card_data: FlipCardCreate,
    db: Session = Depends(get_db)
): 
    """
    This route creates a new flashcard based on the provided data.

    Args:
        card_data: The data used to create the card.
        db (Session): Database session.

    Returns:
        FlipCardResponse: The created card.
    """
    return create_card(db=db, card_data=card_data)
