import pytest
from datetime import date, timedelta

import sys
sys.path.append("..")

from app.models.card import Card
from app.services.srs import update_card_schedule
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSM2Algorithm:
    
    def test_new_card_bad_quality_resets_counter(self):
        """Новая карточка с плохой оценкой (качество < 3)"""
        card = Card(
            question="Test",
            answer="Test",
            repetitions=0,
            interval=1,
            ease_factor=2.5
        )
        
        update_card_schedule(card, quality=2)
        
        assert card.repetitions == 0
        assert card.interval == 1
        assert card.next_review == date.today() + timedelta(days=1)
    
    def test_new_card_good_quality_first_repetition(self):
        """Новая карточка с хорошей оценкой (качество >= 3)"""
        card = Card(
            question="Test",
            answer="Test",
            repetitions=0,
            interval=1,
            ease_factor=2.5
        )
        
        update_card_schedule(card, quality=4)
        
        assert card.repetitions == 1
        assert card.interval == 1
        assert card.ease_factor >= 1.3
    
    def test_second_repetition_interval_6(self):
        """Второе успешное повторение — интервал = 6 дней"""
        card = Card(
            question="Test",
            answer="Test",
            repetitions=1,
            interval=1,
            ease_factor=2.5
        )
        
        update_card_schedule(card, quality=5)
        
        assert card.repetitions == 2
        assert card.interval == 6
    
    def test_ease_factor_never_less_than_1_3(self):
        """Коэффициент лёгкости не может быть меньше 1.3"""
        card = Card(
            question="Test",
            answer="Test",
            repetitions=5,
            interval=10,
            ease_factor=1.3
        )
        
        update_card_schedule(card, quality=1)  # очень плохая оценка
        
        assert card.ease_factor >= 1.3