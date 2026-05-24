<template>
  <div style="padding: 20px; max-width: 800px; margin: 0 auto">
    <!-- Кнопка назад -->
    <button @click="router.back()" style="margin-bottom: 16px; cursor: pointer">
      ← Назад
    </button>

    <!-- Если нет карточек -->
    <div v-if="dueCards.length === 0 && !loading" style="text-align: center; padding: 60px">
      <h2>🎉 Отлично!</h2>
      <p>На сегодня нет карточек для повторения.</p>
      <button @click="router.push('/')" style="padding: 8px 16px; margin-top: 16px; cursor: pointer">
        На главную
      </button>
    </div>

    <!-- Сессия повторения -->
    <div v-else-if="currentCard">
      <!-- Прогресс -->
      <div style="margin-bottom: 20px; color: #666">
        Карточка {{ currentIndex + 1 }} из {{ dueCards.length }}
      </div>

      <!-- Карточка с вопросом -->
      <div style="
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px
      ">
        <h2 style="margin: 0 0 20px 0; font-size: 24px">{{ currentCard.question }}</h2>

        <!-- Поле ввода ответа (режим вопроса) -->
        <div v-if="!showAnswer">
          <textarea
            v-model="userAnswer"
            placeholder="Введите ваш ответ..."
            rows="4"
            style="width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; resize: vertical"
          ></textarea>
          <button @click="checkAnswer" style="
            margin-top: 16px;
            padding: 10px 24px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px
          ">
            Проверить
          </button>
        </div>

        <!-- Режим ответа + оценка -->
        <div v-else>
          <div style="
            background: #f0f8ff;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: left
          ">
            <div><strong>Правильный ответ:</strong></div>
            <div style="margin-top: 8px">{{ currentCard.answer }}</div>
            <div v-if="userAnswer" style="margin-top: 12px">
              <strong>Ваш ответ:</strong> {{ userAnswer }}
            </div>
          </div>

          <div>
            <div style="margin-bottom: 16px; font-weight: bold">Как вы оцениваете?</div>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap">
              <button
                v-for="quality in qualityOptions"
                :key="quality.value"
                @click="submitReview(quality.value)"
                style="
                  padding: 10px 20px;
                  border: none;
                  border-radius: 8px;
                  cursor: pointer;
                  font-size: 14px
                "
                :style="{ backgroundColor: quality.color, color: 'white' }"
              >
                {{ quality.label }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-else-if="loading" style="text-align: center; padding: 60px">
      Загрузка карточек...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCardStore } from '../stores/card'

const router = useRouter()
const cardStore = useCardStore()

const dueCards = ref([])
const loading = ref(true)
const currentIndex = ref(0)
const currentCard = ref(null)
const showAnswer = ref(false)
const userAnswer = ref('')

const qualityOptions = [
  { value: 1, label: '1 — Снова', color: '#e74c3c' },
  { value: 2, label: '2 — Трудно', color: '#e67e22' },
  { value: 3, label: '3 — Средне', color: '#f39c12' },
  { value: 4, label: '4 — Хорошо', color: '#2ecc71' },
  { value: 5, label: '5 — Легко', color: '#27ae60' }
]

onMounted(async () => {
  await loadDueCards()
})

const loadDueCards = async () => {
  loading.value = true
  try {
    dueCards.value = await cardStore.fetchDueCards()
    if (dueCards.value.length > 0) {
      currentCard.value = dueCards.value[0]
      currentIndex.value = 0
    }
  } catch (error) {
    console.error('Failed to load due cards:', error)
  } finally {
    loading.value = false
  }
}

const checkAnswer = () => {
  showAnswer.value = true
}

const submitReview = async (quality) => {
  try {
    await cardStore.submitReview(currentCard.value.id, quality)

    // Переход к следующей карточке
    if (currentIndex.value + 1 < dueCards.value.length) {
      currentIndex.value++
      currentCard.value = dueCards.value[currentIndex.value]
      showAnswer.value = false
      userAnswer.value = ''
    } else {
      // Сессия завершена
      dueCards.value = []
      currentCard.value = null
      showAnswer.value = false
      userAnswer.value = ''
    }
  } catch (error) {
    console.error('Failed to submit review:', error)
    alert('Ошибка при сохранении оценки')
  }
}
</script>