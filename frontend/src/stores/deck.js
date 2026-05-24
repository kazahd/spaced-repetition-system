import { defineStore } from 'pinia'
import api from '../api/axios'

export const useDeckStore = defineStore('deck', {
  state: () => ({
    decks: [],
    loading: false
  }),

  actions: {
    async fetchDecks() {
      this.loading = true
      try {
        const response = await api.get('/decks/')
        this.decks = response.data
      } catch (error) {
        console.error('Fetch decks error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDeck(deckData) {
      const response = await api.post('/decks/', deckData)
      this.decks.push(response.data)
      return response.data
    },

    async updateDeck(deckId, deckData) {
      const response = await api.put(`/decks/${deckId}`, deckData)
      const index = this.decks.findIndex(d => d.id === deckId)
      if (index !== -1) this.decks[index] = response.data
      return response.data
    },

    async deleteDeck(deckId) {
      await api.delete(`/decks/${deckId}`)
      this.decks = this.decks.filter(d => d.id !== deckId)
    }
  }
})