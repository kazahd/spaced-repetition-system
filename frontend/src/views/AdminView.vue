<template>
  <div style="padding: 20px; max-width: 1400px; margin: 0 auto">
    <!-- Кнопка назад -->
    <button @click="router.back()" style="margin-bottom: 20px; cursor: pointer">
      ← Назад
    </button>

    <h1 style="margin-bottom: 24px">👑 Админ-панель</h1>

    <!-- Вкладки -->
    <div style="display: flex; gap: 8px; margin-bottom: 24px; border-bottom: 1px solid #ddd">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :style="{
          padding: '10px 20px',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontSize: '14px',
          borderBottom: activeTab === tab.key ? '2px solid #3498db' : 'none',
          color: activeTab === tab.key ? '#3498db' : '#666',
          fontWeight: activeTab === tab.key ? 'bold' : 'normal'
        }"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Вкладка: Пользователи -->
    <div v-if="activeTab === 'users'">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <h2>Пользователи</h2>
        <button @click="adminStore.fetchUsers()" style="padding: 6px 12px; cursor: pointer">
          Обновить
        </button>
      </div>

      <div v-if="adminStore.loading">Загрузка...</div>

      <div v-else style="overflow-x: auto">
        <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <thead style="background: #f8f9fa">
            <tr>
              <th style="padding: 12px; text-align: left">ID</th>
              <th style="padding: 12px; text-align: left">Логин</th>
              <th style="padding: 12px; text-align: left">Email</th>
              <th style="padding: 12px; text-align: left">Роль</th>
              <th style="padding: 12px; text-align: left">Статус</th>
              <th style="padding: 12px; text-align: left">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in adminStore.users" :key="user.id" style="border-top: 1px solid #eee">
              <td style="padding: 12px">{{ user.id }}</td>
              <td style="padding: 12px">{{ user.username }}</td>
              <td style="padding: 12px">{{ user.email }}</td>
              <td style="padding: 12px">
                <span :style="{
                  padding: '2px 8px',
                  borderRadius: '20px',
                  fontSize: '12px',
                  background: user.role === 'ADMIN' ? '#e74c3c' : '#3498db',
                  color: 'white'
                }">
                  {{ user.role }}
                </span>
              </td>
              <td style="padding: 12px">
                <span :style="{
                  padding: '2px 8px',
                  borderRadius: '20px',
                  fontSize: '12px',
                  background: user.is_blocked ? '#e74c3c' : '#2ecc71',
                  color: 'white'
                }">
                  {{ user.is_blocked ? 'Заблокирован' : 'Активен' }}
                </span>
              </td>
              <td style="padding: 12px">
                <button
                  v-if="user.role !== 'ADMIN'"
                  @click="toggleBlock(user)"
                  :style="{
                    padding: '6px 12px',
                    background: user.is_blocked ? '#2ecc71' : '#e74c3c',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                  }"
                >
                  {{ user.is_blocked ? 'Разблокировать' : 'Заблокировать' }}
                </button>
                <span v-else style="color: #999; font-size: 12px">Системный</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Вкладка: Логи -->
    <div v-if="activeTab === 'logs'">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px">
        <h2>Журнал действий</h2>
        <button @click="adminStore.fetchLogs()" style="padding: 6px 12px; cursor: pointer">
          Обновить
        </button>
      </div>

      <div style="overflow-x: auto">
        <table style="width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <thead style="background: #f8f9fa">
            <tr>
              <th style="padding: 12px; text-align: left">ID</th>
              <th style="padding: 12px; text-align: left">Пользователь</th>
              <th style="padding: 12px; text-align: left">Действие</th>
              <th style="padding: 12px; text-align: left">IP-адрес</th>
              <th style="padding: 12px; text-align: left">Дата и время</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in adminStore.logs" :key="log.id" style="border-top: 1px solid #eee">
              <td style="padding: 12px">{{ log.id }}</td>
              <td style="padding: 12px">{{ log.user_id || 'Аноним' }}</td>
              <td style="padding: 12px; font-family: monospace; font-size: 12px">{{ log.action }}</td>
              <td style="padding: 12px">{{ log.ip_address || '-' }}</td>
              <td style="padding: 12px; font-size: 12px">{{ formatDate(log.created_at) }}</td>
            </tr>
            <tr v-if="adminStore.logs.length === 0">
              <td colspan="5" style="padding: 40px; text-align: center; color: #999">
                Нет записей в журнале
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Вкладка: Системная статистика -->
    <div v-if="activeTab === 'stats'">
      <h2>Системная статистика</h2>

      <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px">
        <div style="flex: 1; min-width: 200px; background: white; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 48px; font-weight: bold; color: #3498db">{{ adminStore.systemStats.total_users || 0 }}</div>
          <div style="color: #666; margin-top: 8px">Всего пользователей</div>
        </div>

        <div style="flex: 1; min-width: 200px; background: white; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 48px; font-weight: bold; color: #2ecc71">{{ adminStore.systemStats.active_users || 0 }}</div>
          <div style="color: #666; margin-top: 8px">Активных пользователей</div>
        </div>

        <div style="flex: 1; min-width: 200px; background: white; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 48px; font-weight: bold; color: #e74c3c">{{ adminStore.systemStats.blocked_users || 0 }}</div>
          <div style="color: #666; margin-top: 8px">Заблокированных</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '../stores/admin'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const adminStore = useAdminStore()
const authStore = useAuthStore()

const activeTab = ref('users')
const tabs = [
  { key: 'users', label: 'Пользователи' },
  { key: 'logs', label: 'Журнал действий' },
  { key: 'stats', label: 'Системная статистика' }
]

onMounted(async () => {
  // Проверяем, что пользователь админ
  if (!authStore.isAdmin) {
    router.push('/')
    return
  }

  await Promise.all([
    adminStore.fetchUsers(),
    adminStore.fetchLogs(),
    adminStore.fetchSystemStats()
  ])
})

const toggleBlock = async (user) => {
  if (user.is_blocked) {
    await adminStore.unblockUser(user.id)
  } else {
    await adminStore.blockUser(user.id)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>