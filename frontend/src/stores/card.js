import { defineStore } from 'pinia'
import api from '../api/axios'

export const useCardStore = defineStore('card', {
  state: () => ({
    cards: [],
    loading: false,
    dueCards: []
  }),

  actions: {
    async fetchCards(deckId) {
      this.loading = true
      try {
        const response = await api.get(`/cards/${deckId}`)
        this.cards = response.data
        return response.data
      } catch (error) {
        console.error('Fetch cards error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchDueCards() {
      try {
        const response = await api.get('/cards/due')
        this.dueCards = response.data
        return response.data
      } catch (error) {
        console.error('Fetch due cards error:', error)
        throw error
      }
    },

    async submitReview(cardId, quality) {
      const response = await api.post(`/reviews/${cardId}`, { quality })
      return response.data
    },

    async createCard(deckId, cardData) {
      const response = await api.post('/cards/', cardData, {
        params: { deck_id: deckId }
      })
      this.cards.push(response.data)
      return response.data
    },

    async updateCard(cardId, cardData) {
      const response = await api.put(`/cards/${cardId}`, cardData)
      const index = this.cards.findIndex(c => c.id === cardId)
      if (index !== -1) this.cards[index] = response.data
      return response.data
    },

    async deleteCard(cardId) {
      await api.delete(`/cards/${cardId}`)
      this.cards = this.cards.filter(c => c.id !== cardId)
    },

  async toggleCard(cardId) {
    const response = await api.patch(`/cards/${cardId}/toggle`)
    const index = this.cards.findIndex(c => c.id === cardId)
    if (index !== -1) this.cards[index] = response.data
    return response.data
}
  }
})