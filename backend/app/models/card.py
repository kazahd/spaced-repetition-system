from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    deck_id = Column(Integer, ForeignKey("decks.id"))

    repetitions = Column(Integer, default=0)
    interval = Column(Integer, default=1)

    ease_factor = Column(Float, default=2.5)

    next_review = Column(Date)

    is_active = Column(Boolean, default=True)

    deck = relationship("Deck", back_populates="cards")

    reviews = relationship("Review", back_populates="card", cascade="all, delete")