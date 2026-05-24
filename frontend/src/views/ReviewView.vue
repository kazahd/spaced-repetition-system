<template>
  <div style="padding: 20px">
    <button @click="router.back()" style="margin-bottom: 16px; cursor: pointer">← Назад</button>
    <h1>Сессия повторения</h1>
    <p>Страница в разработке</p>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>