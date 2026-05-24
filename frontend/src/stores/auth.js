import { defineStore } from 'pinia'

import api from '../api/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'ADMIN'
  },

  actions: {
    async login(username, password) {
      const formData = new URLSearchParams()

      formData.append('username', username)
      formData.append('password', password)

      const response = await api.post(
        '/auth/login',
        formData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )

      this.token = response.data.access_token

      localStorage.setItem(
        'token',
        this.token
      )

      await this.fetchUser()
    },

    async register(data) {
      await api.post('/auth/register', data)
    },

    async fetchUser() {
      const response = await api.get('/users/me')

      this.user = response.data
    },

    logout() {
      this.token = null
      this.user = null

      localStorage.removeItem('token')
    }
  }
})