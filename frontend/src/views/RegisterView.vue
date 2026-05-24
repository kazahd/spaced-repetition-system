<template>
  <div>
    <h1>Register</h1>

    <form @submit.prevent="handleRegister">

      <input
        v-model="username"
        placeholder="Username"
      />

      <input
        v-model="email"
        placeholder="Email"
      />

      <input
        v-model="password"
        type="password"
        placeholder="Password"
      />

      <button type="submit">
        Register
      </button>

    </form>

    <p v-if="success">
      Registration successful
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
const email = ref('')
const password = ref('')

const success = ref(false)

const handleRegister = async () => {
  await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value
  })

  success.value = true

  router.push('/login')
}
</script>