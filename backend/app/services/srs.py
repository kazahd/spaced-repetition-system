from datetime import date, timedelta

from app.models.card import Card

def update_card_schedule(card: Card, quality: int):
    """
    SM-2 algorithm
    """

    if quality < 3:
        card.repetitions = 0
        card.interval = 1

    else:
        if card.repetitions == 0:
            card.interval = 1

        elif card.repetitions == 1:
            card.interval = 6

        else:
            card.interval = int(
                card.interval * card.ease_factor
            )

        card.repetitions += 1
        
    card.ease_factor = max(
        1.3,
        card.ease_factor + (
            0.1 - (5 - quality) * (
                0.08 + (5 - quality) * 0.02
            )
        )
    )

    card.next_review = (
        date.today() + timedelta(days=card.interval)
    )

    return card