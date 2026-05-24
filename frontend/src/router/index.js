import { createRouter, createWebHistory } from 'vue-router'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'

const routes = [
  {
    path: '/login',
    component: LoginView,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    component: RegisterView,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  {
    path: '/decks/:id',
    component: () => import('../views/DeckDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/review',
    component: () => import('../views/ReviewView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/review',
    component: () => import('../views/ReviewView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/stats',
    component: () => import('../views/StatisticsView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router