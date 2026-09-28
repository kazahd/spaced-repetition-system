from datetime import date

from pydantic import BaseModel


class CardCreate(BaseModel):
    question: str
    answer: str


class CardResponse(BaseModel):
    id: int

    question: str
    answer: str

    repetitions: int
    interval: int
    ease_factor: float

    next_review: date | None

    deck_id: int

    is_active: bool
    class Config:
        from_attributes = True