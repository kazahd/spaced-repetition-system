from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.card import Card
from app.models.user import User
from app.models.review import Review

from app.schemas.review import ReviewRequest

from app.core.dependencies import get_current_user

from app.services.srs import update_card_schedule


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/{card_id}")
def review_card(
    card_id: int,
    review: ReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    card = db.query(Card).filter(
        Card.id == card_id
    ).first()

    if not card:
        raise HTTPException(
            status_code=404,
            detail="Card not found"
        )

    # обновляем карточку по SM-2
    update_card_schedule(
        card,
        review.quality
    )

    # сохраняем историю review
    review_log = Review(
        user_id=current_user.id,
        card_id=card.id,
        quality=review.quality
    )

    db.add(review_log)

    db.commit()

    db.refresh(card)

    return {
        "message": "Review saved",
        "next_review": card.next_review,
        "interval": card.interval,
        "ease_factor": card.ease_factor
    }