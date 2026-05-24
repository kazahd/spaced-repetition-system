<template>
  <div style="padding: 20px; max-width: 1200px; margin: 0 auto">
    <!-- Шапка -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h1>Мои колоды</h1>
      <div style="display: flex; gap: 12px">
        <button @click="goToReview" style="
          padding: 8px 16px;
          background-color: #9b59b6;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px
        ">
          📖 Повторение
        </button>
        <button @click="goToStats" style="
          padding: 8px 16px;
          background-color: #2ecc71;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px
        ">
          📊 Статистика
        </button>
        <button v-if="authStore.isAdmin" @click="goToAdmin" style="
          padding: 8px 16px;
          background-color: #e74c3c;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px
        ">
          👑 Админка
        </button>
        <button @click="logout" style="
          padding: 8px 16px;
          background-color: #95a5a6;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px
        ">
          Выйти
        </button>
      </div>
    </div>

    <!-- Сегодня на повторение -->
    <div style="
      background-color: #f8f9fa;
      padding: 16px 20px;
      border-radius: 8px;
      margin-bottom: 24px;
      border-left: 4px solid #9b59b6
    ">
      <div style="display: flex; justify-content: space-between; align-items: center">
        <div>
          <span style="font-size: 14px; color: #666">Сегодня на повторение</span>
          <div style="font-size: 32px; font-weight: bold; line-height: 1.2">{{ dueCardsCount }}</div>
        </div>
        <button @click="goToReview" style="
          padding: 8px 20px;
          background-color: #9b59b6;
          color: white;
          border: none;
          border-radius: 4px;
          cursor: pointer
        ">
          Начать повторение
        </button>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="deckStore.loading" style="text-align: center; padding: 40px">
      Загрузка колод...
    </div>

    <!-- Список колод -->
    <div v-else style="display: flex; flex-wrap: wrap; gap: 16px">
      <div v-for="deck in deckStore.decks" :key="deck.id" style="
        width: 280px;
        padding: 16px;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: box-shadow 0.2s
      ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start">
          <h3 style="margin: 0 0 8px 0; font-size: 18px; flex: 1">{{ deck.title }}</h3>
          <div style="display: flex; gap: 8px">
            <button 
              @click.stop="openEditModal(deck)" 
              style="
                background: none;
                border: none;
                color: #f39c12;
                font-size: 18px;
                cursor: pointer;
                opacity: 0.6
              "
              title="Редактировать колоду"
            >
              ✏️
            </button>
            <button 
              @click.stop="deleteDeck(deck.id)" 
              style="
                background: none;
                border: none;
                color: #e74c3c;
                font-size: 18px;
                cursor: pointer;
                opacity: 0.6
              "
              title="Удалить колоду"
            >
              🗑️
            </button>
          </div>
        </div>
        <p style="margin: 0 0 12px 0; color: #666; font-size: 14px">
          {{ deck.description || 'Нет описания' }}
        </p>
        <div style="display: flex; justify-content: flex-end; margin-top: 8px">
          <button 
            @click="viewDeck(deck.id)" 
            style="
              padding: 6px 16px;
              background-color: #3498db;
              color: white;
              border: none;
              border-radius: 4px;
              cursor: pointer;
              font-size: 12px
            "
          >
            Открыть
          </button>
        </div>
      </div>

      <!-- Карточка создания новой колоды -->
      <div @click="showCreateModal = true" style="
        width: 280px;
        padding: 16px;
        border: 2px dashed #ccc;
        border-radius: 12px;
        background: #fafafa;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 120px;
        cursor: pointer;
        transition: all 0.2s
      ">
        <div style="font-size: 32px; color: #ccc">+</div>
        <div style="color: #999; margin-top: 8px">Создать колоду</div>
      </div>

      <!-- Если колод нет -->
      <div v-if="deckStore.decks.length === 0 && !deckStore.loading" style="width: 100%; text-align: center; padding: 60px; color: #999">
        У вас пока нет колод. Нажмите «Создать колоду», чтобы начать.
      </div>
    </div>

    <!-- Модальное окно создания колоды -->
    <div v-if="showCreateModal" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000
    ">
      <div style="
        background: white;
        padding: 24px;
        border-radius: 12px;
        width: 450px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2)
      ">
        <h2 style="margin: 0 0 20px 0">Создать колоду</h2>
        <div style="margin-bottom: 16px">
          <label style="display: block; margin-bottom: 6px; font-weight: 500">Название <span style="color: #e74c3c">*</span></label>
          <input
            v-model="newDeck.title"
            type="text"
            placeholder="Например: Английские слова"
            style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px"
            @keyup.enter="createDeck"
          />
        </div>
        <div style="margin-bottom: 20px">
          <label style="display: block; margin-bottom: 6px; font-weight: 500">Описание</label>
          <input
            v-model="newDeck.description"
            type="text"
            placeholder="Необязательно"
            style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px"
            @keyup.enter="createDeck"
          />
        </div>
        <div style="display: flex; gap: 12px; justify-content: flex-end">
          <button @click="closeCreateModal" style="
            padding: 8px 16px;
            background: none;
            border: 1px solid #ddd;
            border-radius: 6px;
            cursor: pointer
          ">
            Отмена
          </button>
          <button @click="createDeck" style="
            padding: 8px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer
          ">
            Создать
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно редактирования колоды -->
    <div v-if="showEditModal" style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 1000
    ">
      <div style="
        background: white;
        padding: 24px;
        border-radius: 12px;
        width: 450px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2)
      ">
        <h2 style="margin: 0 0 20px 0">Редактировать колоду</h2>
        <div style="margin-bottom: 16px">
          <label style="display: block; margin-bottom: 6px; font-weight: 500">Название <span style="color: #e74c3c">*</span></label>
          <input
            v-model="editDeck.title"
            type="text"
            placeholder="Название"
            style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px"
            @keyup.enter="updateDeck"
          />
        </div>
        <div style="margin-bottom: 20px">
          <label style="display: block; margin-bottom: 6px; font-weight: 500">Описание</label>
          <input
            v-model="editDeck.description"
            type="text"
            placeholder="Необязательно"
            style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px"
            @keyup.enter="updateDeck"
          />
        </div>
        <div style="display: flex; gap: 12px; justify-content: flex-end">
          <button @click="closeEditModal" style="
            padding: 8px 16px;
            background: none;
            border: 1px solid #ddd;
            border-radius: 6px;
            cursor: pointer
          ">
            Отмена
          </button>
          <button @click="updateDeck" style="
            padding: 8px 20px;
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer
          ">
            Сохранить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDeckStore } from '../stores/deck'
import { useCardStore } from '../stores/card'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const deckStore = useDeckStore()
const cardStore = useCardStore()
const authStore = useAuthStore()

const showCreateModal = ref(false)
const showEditModal = ref(false)
const newDeck = ref({ title: '', description: '' })
const editDeck = ref({ id: null, title: '', description: '' })
const dueCardsCount = ref(0)

onMounted(async () => {
  await Promise.all([
    deckStore.fetchDecks(),
    loadDueCardsCount()
  ])
})

const loadDueCardsCount = async () => {
  try {
    const dueCards = await cardStore.fetchDueCards()
    dueCardsCount.value = dueCards.length
  } catch (error) {
    console.error('Failed to load due cards:', error)
    dueCardsCount.value = 0
  }
}

const createDeck = async () => {
  if (!newDeck.value.title.trim()) {
    alert('Введите название колоды')
    return
  }
  await deckStore.createDeck({
    title: newDeck.value.title.trim(),
    description: newDeck.value.description || null
  })
  newDeck.value = { title: '', description: '' }
  showCreateModal.value = false
}

const closeCreateModal = () => {
  showCreateModal.value = false
  newDeck.value = { title: '', description: '' }
}

const openEditModal = (deck) => {
  editDeck.value = {
    id: deck.id,
    title: deck.title,
    description: deck.description || ''
  }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editDeck.value = { id: null, title: '', description: '' }
}

const updateDeck = async () => {
  if (!editDeck.value.title.trim()) {
    alert('Введите название колоды')
    return
  }
  await deckStore.updateDeck(editDeck.value.id, {
    title: editDeck.value.title.trim(),
    description: editDeck.value.description || null
  })
  closeEditModal()
}

const viewDeck = (deckId) => {
  router.push(`/decks/${deckId}`)
}

const deleteDeck = async (deckId) => {
  if (confirm('Удалить колоду? Все карточки внутри тоже будут удалены.')) {
    await deckStore.deleteDeck(deckId)
    await loadDueCardsCount()
  }
}

const goToReview = () => {
  router.push('/review')
}

const goToStats = () => {
  router.push('/stats')
}

const goToAdmin = () => {
  router.push('/admin')
}

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>