<template>
  <div style="padding: 20px">
    <button @click="router.back()" style="margin-bottom: 16px">← Назад</button>
    <h1>Карточки колоды</h1>
    <p>Страница в разработке. Deck ID: {{ deckId }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const deckId = ref(null)

onMounted(() => {
  deckId.value = route.params.id
})
</script>