import { defineStore } from 'pinia'
import api from '../api/axios'

export const useStatisticsStore = defineStore('statistics', {
  state: () => ({
    stats: {
      total_cards: 0,
      total_decks: 0,
      total_reviews: 0,
      reviews_today: 0,
      reviews_by_day: []
    },
    loading: false
  }),

  actions: {
    async fetchStats() {
      this.loading = true
      try {
        const response = await api.get('/stats/')
        this.stats = response.data
        return response.data
      } catch (error) {
        console.error('Fetch stats error:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})