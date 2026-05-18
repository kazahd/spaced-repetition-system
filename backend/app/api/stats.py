from datetime import date

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.session import get_db

from app.models.card import Card
from app.models.deck import Deck
from app.models.review import Review
from app.models.user import User

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/stats",
    tags=["Stats"]
)


@router.get("/")
def get_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # карточки
    total_cards = (
        db.query(Card)
        .join(Card.deck)
        .filter(
            Deck.owner_id == current_user.id
        )
        .count()
    )

    # колоды
    total_decks = (
        db.query(Deck)
        .filter(
            Deck.owner_id == current_user.id
        )
        .count()
    )

    # все повторения
    total_reviews = (
        db.query(Review)
        .filter(
            Review.user_id == current_user.id
        )
        .count()
    )

    # повторения сегодня
    reviews_today = (
        db.query(Review)
        .filter(
            Review.user_id == current_user.id,
            func.date(Review.reviewed_at) == date.today()
        )
        .count()
    )

    # график повторений по дням
    reviews_by_day_query = (
        db.query(
            func.date(Review.reviewed_at),
            func.count(Review.id)
        )
        .filter(
            Review.user_id == current_user.id
        )
        .group_by(
            func.date(Review.reviewed_at)
        )
        .order_by(
            func.date(Review.reviewed_at)
        )
        .all()
    )

    reviews_by_day = [
        {
            "date": str(day),
            "count": count
        }
        for day, count in reviews_by_day_query
    ]

    return {
        "total_cards": total_cards,
        "total_decks": total_decks,
        "total_reviews": total_reviews,
        "reviews_today": reviews_today,
        "reviews_by_day": reviews_by_day
    }