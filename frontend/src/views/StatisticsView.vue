<template>
  <div style="padding: 20px; max-width: 1200px; margin: 0 auto">
    <!-- Кнопка назад -->
    <button @click="router.back()" style="margin-bottom: 20px; cursor: pointer">
      ← Назад
    </button>

    <h1 style="margin-bottom: 24px">Статистика</h1>

    <!-- Загрузка -->
    <div v-if="statsStore.loading" style="text-align: center; padding: 60px">
      Загрузка...
    </div>

    <div v-else>
      <!-- Карточки с общей статистикой -->
      <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 32px">
        <div style="flex: 1; min-width: 150px; background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 36px; font-weight: bold; color: #3498db">{{ statsStore.stats.total_decks }}</div>
          <div style="color: #666; margin-top: 8px">Колод</div>
        </div>

        <div style="flex: 1; min-width: 150px; background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 36px; font-weight: bold; color: #2ecc71">{{ statsStore.stats.total_cards }}</div>
          <div style="color: #666; margin-top: 8px">Карточек</div>
        </div>

        <div style="flex: 1; min-width: 150px; background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 36px; font-weight: bold; color: #9b59b6">{{ statsStore.stats.total_reviews }}</div>
          <div style="color: #666; margin-top: 8px">Всего повторений</div>
        </div>

        <div style="flex: 1; min-width: 150px; background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
          <div style="font-size: 36px; font-weight: bold; color: #e74c3c">{{ statsStore.stats.reviews_today }}</div>
          <div style="color: #666; margin-top: 8px">Повторений сегодня</div>
        </div>
      </div>

      <!-- График -->
      <div style="background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
        <h3 style="margin-bottom: 20px">Динамика повторений</h3>
        <canvas ref="chartCanvas" style="max-height: 400px; width: 100%"></canvas>
        <div v-if="statsStore.stats.reviews_by_day.length === 0" style="text-align: center; padding: 40px; color: #999">
          Нет данных для отображения графика
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStatisticsStore } from '../stores/statistics'
import Chart from 'chart.js/auto'

const router = useRouter()
const statsStore = useStatisticsStore()
const chartCanvas = ref(null)
let chartInstance = null

onMounted(async () => {
  await statsStore.fetchStats()
  createChart()
})

const createChart = () => {
  const reviewsByDay = statsStore.stats.reviews_by_day
  
  if (!reviewsByDay || reviewsByDay.length === 0) return

  const labels = reviewsByDay.map(item => item.date)
  const data = reviewsByDay.map(item => item.count)

  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = chartCanvas.value.getContext('2d')
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Количество повторений',
          data: data,
          borderColor: '#3498db',
          backgroundColor: 'rgba(52, 152, 219, 0.1)',
          borderWidth: 2,
          fill: true,
          tension: 0.3,
          pointBackgroundColor: '#3498db',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.raw} повторений`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            precision: 0
          },
          title: {
            display: true,
            text: 'Количество повторений'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Дата'
          }
        }
      }
    }
  })
}
</script>