<template>
  <div style="padding: 20px">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px">
      <h1>Мои колоды</h1>
      <button @click="showCreateModal = true" style="
        padding: 8px 16px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      ">
        + Создать колоду
      </button>
    </div>

    <!-- Загрузка -->
    <div v-if="deckStore.loading">Загрузка...</div>

    <!-- Список колод -->
    <div v-else style="display: flex; flex-wrap: wrap; gap: 16px">
      <div v-for="deck in deckStore.decks" :key="deck.id" style="
        width: 250px;
        padding: 16px;
        border: 1px solid #ddd;
        border-radius: 8px;
        background: white;
      ">
        <h3 style="margin: 0 0 8px 0">{{ deck.title }}</h3>
        <p style="margin: 0 0 8px 0; color: #666">{{ deck.description || 'Нет описания' }}</p>
        <div style="display: flex; gap: 8px; justify-content: flex-end">
          <button @click="viewDeck(deck.id)" style="
            padding: 4px 12px;
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          ">
            Открыть
          </button>
          <button @click="deleteDeck(deck.id)" style="
            padding: 4px 12px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
          ">
            Удалить
          </button>
        </div>
      </div>

      <!-- Если колод нет -->
      <div v-if="deckStore.decks.length === 0" style="color: #666">
        Нет колод. Создайте первую колоду!
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
    ">
      <div style="
        background: white;
        padding: 24px;
        border-radius: 8px;
        width: 400px;
      ">
        <h2>Создать колоду</h2>
        <input
          v-model="newDeck.title"
          placeholder="Название"
          style="width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px"
        />
        <input
          v-model="newDeck.description"
          placeholder="Описание (необязательно)"
          style="width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px"
        />
        <div style="display: flex; gap: 8px; justify-content: flex-end; margin-top: 16px">
          <button @click="showCreateModal = false" style="padding: 6px 12px">Отмена</button>
          <button @click="createDeck" style="padding: 6px 12px; background-color: #3498db; color: white; border: none; border-radius: 4px">Создать</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDeckStore } from '../stores/deck'

const router = useRouter()
const deckStore = useDeckStore()

const showCreateModal = ref(false)
const newDeck = ref({ title: '', description: '' })

onMounted(async () => {
  await deckStore.fetchDecks()
})

const createDeck = async () => {
  if (!newDeck.value.title.trim()) {
    alert('Введите название колоды')
    return
  }
  await deckStore.createDeck(newDeck.value)
  newDeck.value = { title: '', description: '' }
  showCreateModal.value = false
}

const viewDeck = (deckId) => {
  router.push(`/decks/${deckId}`)
}

const deleteDeck = async (deckId) => {
  if (confirm('Удалить колоду? Все карточки внутри тоже удалятся.')) {
    await deckStore.deleteDeck(deckId)
  }
}
</script>