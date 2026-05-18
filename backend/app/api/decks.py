from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.deck import Deck
from app.models.user import User

from app.schemas.deck import (
    DeckCreate,
    DeckResponse
)

from app.api.dependencies import get_current_user


router = APIRouter(
    prefix="/decks",
    tags=["Decks"]
)


@router.post("/", response_model=DeckResponse)
def create_deck(
    deck_data: DeckCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deck = Deck(
        title=deck_data.title,
        description=deck_data.description,
        owner_id=current_user.id
    )

    db.add(deck)
    db.commit()
    db.refresh(deck)

    return deck


@router.get("/", response_model=list[DeckResponse])
def get_my_decks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decks = db.query(Deck).filter(
        Deck.owner_id == current_user.id
    ).all()

    return decks