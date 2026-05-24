<template>
  <div style="padding: 20px">
    <!-- Кнопка назад -->
    <button @click="router.back()" style="margin-bottom: 16px; padding: 6px 12px; cursor: pointer">
      ← Назад
    </button>

    <!-- Заголовок -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h1>{{ deckTitle }}</h1>
      <button @click="showCreateModal = true" style="
        padding: 8px 16px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer
      ">
        + Добавить карточку
      </button>
    </div>

    <!-- Загрузка -->
    <div v-if="cardStore.loading">Загрузка...</div>

    <!-- Список карточек -->
    <div v-else style="display: flex; flex-direction: column; gap: 12px">
      <div v-for="card in cardStore.cards" :key="card.id" style="
        padding: 16px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
        display: flex;
        justify-content: space-between;
        align-items: center
      ">
        <div style="flex: 1">
          <div><strong>Вопрос:</strong> {{ card.question }}</div>
          <div style="margin-top: 8px; color: #666"><strong>Ответ:</strong> {{ card.answer }}</div>
          <div style="margin-top: 8px; font-size: 12px; color: #999">
            Интервал: {{ card.interval }} дней | Следующее: {{ card.next_review || 'сегодня' }}
          </div>
        </div>
        <div style="display: flex; gap: 8px">
          <button @click="editCard(card)" style="padding: 4px 12px; background-color: #f39c12; color: white; border: none; border-radius: 4px; cursor: pointer">
            ✏️
          </button>
          <button @click="deleteCard(card.id)" style="padding: 4px 12px; background-color: #e74c3c; color: white; border: none; border-radius: 4px; cursor: pointer">
            🗑️
          </button>
        </div>
      </div>

      <!-- Если карточек нет -->
      <div v-if="cardStore.cards.length === 0" style="color: #666; text-align: center; padding: 40px">
        Нет карточек. Добавьте первую карточку!
      </div>
    </div>

    <!-- Модальное окно создания карточки -->
    <div v-if="showCreateModal" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center
    ">
      <div style="background: white; padding: 24px; border-radius: 8px; width: 500px">
        <h2>Создать карточку</h2>
        <div style="margin-bottom: 12px">
          <label style="display: block; margin-bottom: 4px; font-weight: bold">Вопрос</label>
          <textarea
            v-model="newCard.question"
            placeholder="Введите вопрос"
            rows="3"
            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; resize: vertical"
          ></textarea>
        </div>
        <div style="margin-bottom: 12px">
          <label style="display: block; margin-bottom: 4px; font-weight: bold">Ответ</label>
          <textarea
            v-model="newCard.answer"
            placeholder="Введите ответ"
            rows="3"
            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; resize: vertical"
          ></textarea>
        </div>
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button @click="showCreateModal = false" style="padding: 6px 12px; cursor: pointer">Отмена</button>
          <button @click="createCard" style="padding: 6px 12px; background-color: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer">Создать</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования карточки -->
    <div v-if="showEditModal" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center
    ">
      <div style="background: white; padding: 24px; border-radius: 8px; width: 500px">
        <h2>Редактировать карточку</h2>
        <div style="margin-bottom: 12px">
          <label style="display: block; margin-bottom: 4px; font-weight: bold">Вопрос</label>
          <textarea
            v-model="editCardData.question"
            rows="3"
            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; resize: vertical"
          ></textarea>
        </div>
        <div style="margin-bottom: 12px">
          <label style="display: block; margin-bottom: 4px; font-weight: bold">Ответ</label>
          <textarea
            v-model="editCardData.answer"
            rows="3"
            style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; resize: vertical"
          ></textarea>
        </div>
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button @click="showEditModal = false" style="padding: 6px 12px; cursor: pointer">Отмена</button>
          <button @click="updateCard" style="padding: 6px 12px; background-color: #2ecc71; color: white; border: none; border-radius: 4px; cursor: pointer">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useDeckStore } from '../stores/deck'
import { useCardStore } from '../stores/card'

const route = useRoute()
const router = useRouter()
const deckStore = useDeckStore()
const cardStore = useCardStore()

const deckId = ref(null)
const deckTitle = ref('')

const showCreateModal = ref(false)
const showEditModal = ref(false)
const newCard = ref({ question: '', answer: '' })
const editCardData = ref({ id: null, question: '', answer: '' })

onMounted(async () => {
  deckId.value = route.params.id
  await Promise.all([
    deckStore.fetchDecks(),
    cardStore.fetchCards(deckId.value)
  ])
  const deck = deckStore.decks.find(d => d.id == deckId.value)
  deckTitle.value = deck?.title || 'Карточки колоды'
})

const createCard = async () => {
  if (!newCard.value.question.trim()) {
    alert('Введите вопрос')
    return
  }
  if (!newCard.value.answer.trim()) {
    alert('Введите ответ')
    return
  }
  await cardStore.createCard(deckId.value, newCard.value)
  newCard.value = { question: '', answer: '' }
  showCreateModal.value = false
}

const editCard = (card) => {
  editCardData.value = {
    id: card.id,
    question: card.question,
    answer: card.answer
  }
  showEditModal.value = true
}

const updateCard = async () => {
  await cardStore.updateCard(editCardData.value.id, {
    question: editCardData.value.question,
    answer: editCardData.value.answer
  })
  showEditModal.value = false
}

const deleteCard = async (cardId) => {
  if (confirm('Удалить карточку?')) {
    await cardStore.deleteCard(cardId)
  }
}
</script>