import { defineStore } from 'pinia'
import api from '../api/axios'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [],
    logs: [],
    systemStats: {},
    loading: false
  }),

  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await api.get('/admin/users')
        this.users = response.data
        return response.data
      } catch (error) {
        console.error('Fetch users error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async blockUser(userId) {
      try {
        const response = await api.post(`/admin/users/${userId}/block`)
        await this.fetchUsers() // обновляем список
        return response.data
      } catch (error) {
        console.error('Block user error:', error)
        throw error
      }
    },

    async unblockUser(userId) {
      try {
        const response = await api.post(`/admin/users/${userId}/unblock`)
        await this.fetchUsers() // обновляем список
        return response.data
      } catch (error) {
        console.error('Unblock user error:', error)
        throw error
      }
    },

    async fetchLogs(limit = 100) {
      try {
        const response = await api.get('/admin/logs', { params: { limit } })
        this.logs = response.data
        return response.data
      } catch (error) {
        console.error('Fetch logs error:', error)
        throw error
      }
    },

    async fetchSystemStats() {
      try {
        const response = await api.get('/admin/stats')
        this.systemStats = response.data
        return response.data
      } catch (error) {
        console.error('Fetch system stats error:', error)
        throw error
      }
    }
  }
})