<template>
  <div style="padding: 40px; max-width: 400px; margin: 0 auto">
    <h1 style="margin-bottom: 24px">Вход</h1>

    <form @submit.prevent="handleLogin">
      <div style="margin-bottom: 16px">
        <input
          v-model="username"
          placeholder="Логин"
          style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px"
        />
      </div>

      <div style="margin-bottom: 16px">
        <input
          v-model="password"
          type="password"
          placeholder="Пароль"
          style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px"
        />
      </div>

      <button
        type="submit"
        style="width: 100%; padding: 10px; background-color: #3498db; color: white; border: none; border-radius: 6px; cursor: pointer"
      >
        Войти
      </button>
    </form>

    <p style="margin-top: 16px; text-align: center">
      Нет аккаунта?
      <router-link to="/register" style="color: #3498db; text-decoration: none">Зарегистрироваться</router-link>
    </p>

    <p v-if="error" style="color: #e74c3c; text-align: center; margin-top: 16px">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (err) {
    error.value = 'Неверный логин или пароль'
  }
}
</script>