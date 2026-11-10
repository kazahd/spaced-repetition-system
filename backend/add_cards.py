"""
Универсальный скрипт для добавления карточек.
Отредактируй список new_cards ниже и запусти скрипт.
"""
from app.db.database import SessionLocal
from app.models.user import User
from app.models.card import Card
from app.models.deck import Deck
from datetime import date


# ============================================================
# НАСТРОЙКИ — меняй только это
# ============================================================

USERNAME = "gaben"
DECK_TITLE = "SQL"

NEW_CARDS = [
    {
        "question": "Что такое вычисляемое поле в SQL? Как его создать?",
        "answer": "Поле, значение которого не хранится в таблице, а вычисляется в запросе.\nSELECT name, price * quantity AS total FROM order_items;\ntotal — вычисляемое поле, его нет в таблице."
    },
    {
        "question": "Что делают CONCAT() и CONCAT_WS()?",
        "answer": "CONCAT(a, b, c) — склеивает значения в строку.\nCONCAT_WS(sep, a, b, c) — склеивает с разделителем sep.\nПример: CONCAT_WS('-', '2025', '01', '15') → '2025-01-15'.\nВ PostgreSQL также работает || для конкатенации."
    },
    {
        "question": "Что будет, если в математическом выражении есть NULL?",
        "answer": "Результат всего выражения — NULL. NULL + 5 = NULL, NULL * 0 = NULL.\nЭто не 0 и не ошибка."
    },
]

# ============================================================
# ============================================================
# НИЖЕ — НЕ ТРОГАЙ (логика скрипта)
# ============================================================


def main():
    if not NEW_CARDS:
        print("⚠️ Список NEW_CARDS пуст. Добавь карточки.")
        return

    db = SessionLocal()
    user = db.query(User).filter(User.username == USERNAME).first()
    if not user:
        print(f"Пользователь {USERNAME} не найден")
        return

    deck = db.query(Deck).filter(
        Deck.owner_id == user.id,
        Deck.title == DECK_TITLE
    ).first()

    if not deck:
        print(f"Колода '{DECK_TITLE}' не найдена у {USERNAME}")
        print("Доступные колоды:")
        for d in db.query(Deck).filter(Deck.owner_id == user.id).all():
            print(f"  - {d.title}")
        return

    added = 0
    for card_data in NEW_CARDS:
        card = Card(
            question=card_data["question"],
            answer=card_data["answer"],
            deck_id=deck.id,
            repetitions=0,
            interval=1,
            ease_factor=2.5,
            next_review=date.today(),
            is_active=True
        )
        db.add(card)
        added += 1

    db.commit()
    print(f"➕ Добавлено карточек: {added}")
    print(f"Колода: {deck.title}")

    total = db.query(Card).filter(Card.deck_id == deck.id).count()
    print(f"Всего в колоде: {total}")


if __name__ == "__main__":
    main()