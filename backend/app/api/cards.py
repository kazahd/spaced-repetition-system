from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.card import Card
from app.models.deck import Deck
from app.models.user import User

from app.schemas.card import (
    CardCreate,
    CardResponse
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/cards",
    tags=["Cards"]
)


@router.post("/", response_model=CardResponse)
def create_card(
    card_data: CardCreate,
    deck_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deck = db.query(Deck).filter(
        Deck.id == deck_id,
        Deck.owner_id == current_user.id
    ).first()

    if not deck:
        raise HTTPException(
            status_code=404,
            detail="Deck not found"
        )

    card = Card(
        question=card_data.question,
        answer=card_data.answer,

        deck_id=deck.id,

        repetitions=0,
        interval=1,
        ease_factor=2.5,

        next_review=date.today()
    )

    db.add(card)

    db.commit()

    db.refresh(card)

    return card

@router.get("/due")
def get_due_cards(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cards = (
        db.query(Card)
        .join(Card.deck)
        .filter(
            Deck.owner_id == current_user.id,
            (
                (Card.next_review <= date.today())
                |
                (Card.next_review == None)
            )
        )
        .all()
    )

    return cards

@router.get("/{deck_id}", response_model=list[CardResponse])
def get_cards(
    deck_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deck = db.query(Deck).filter(
        Deck.id == deck_id,
        Deck.owner_id == current_user.id
    ).first()

    if not deck:
        raise HTTPException(
            status_code=404,
            detail="Deck not found"
        )

    return deck.cards

@router.put("/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    card_data: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Обновить карточку (только владелец колоды)"""
    card = db.query(Card).join(Card.deck).filter(
        Card.id == card_id,
        Deck.owner_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    card.question = card_data.question
    card.answer = card_data.answer
    
    db.commit()
    db.refresh(card)
    
    return card


@router.delete("/{card_id}")
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить карточку (только владелец колоды)"""
    card = db.query(Card).join(Card.deck).filter(
        Card.id == card_id,
        Deck.owner_id == current_user.id
    ).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(card)
    db.commit()
    
    return {"message": "Card deleted successfully"}