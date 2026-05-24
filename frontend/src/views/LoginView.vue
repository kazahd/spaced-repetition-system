<template>
  <div>
    <h1>Login</h1>

    <form @submit.prevent="handleLogin">
      <input
        v-model="username"
        placeholder="Username"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
      />

      <button type="submit">
        Login
      </button>
    </form>

    <p v-if="error">
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
    await authStore.login(
      username.value,
      password.value
    )

    router.push('/')

  } catch (err) {
    error.value = 'Login failed'
  }
}
</script>