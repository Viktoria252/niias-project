<template>
  <div class="home-container">
    <div class="header">
      <h1>Список заявок</h1>
      <button class="btn btn-add" @click="goToAdd">+ Добавить заявку</button>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div class="list-container" v-else>
      <div v-if="applications.length === 0" class="empty-state">
        <p>Пока нет ни одной заявки. Создайте первую!</p>
      </div>

      <ApplicationCard
        v-for="app in applications"
        :key="app.id"
        :application="app"
        @verify="verifyApplication"
        @delete="deleteApplication"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ApplicationCard from '../components/ApplicationCard.vue'
import { api } from '../services/api' // Импортируем наш сервис

const router = useRouter()
const applications = ref([])
const loading = ref(true)

// Загружаем данные при открытии страницы
onMounted(async () => {
  try {
    applications.value = await api.getApplications()
  } catch (error) {
    console.error(error)
    alert('Не удалось загрузить заявки')
  } finally {
    loading.value = false
  }
})

const goToAdd = () => router.push('/add')
const verifyApplication = (id) => router.push(`/verify/${id}`)

const deleteApplication = async (id) => {
  if (confirm('Вы уверены, что хотите удалить заявку?')) {
    try {
      await api.deleteApplication(id)
      // Удаляем из локального массива, чтобы не перезагружать страницу
      applications.value = applications.value.filter(app => app.id !== id)
    } catch (error) {
      alert('Ошибка при удалении')
    }
  }
}
</script>

<style scoped>
/* Стили оставляем как были... */
.home-container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
h1 { margin: 0; color: #111827; }
.list-container { display: flex; flex-direction: column; gap: 15px; }
.btn-add { background-color: #e3000f; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.btn-add:hover { background-color: #c0000c; }
.empty-state { text-align: center; padding: 50px; background: white; border-radius: 8px; color: #6b7280; border: 2px dashed #e5e7eb; }
.loading { text-align: center; padding: 50px; font-size: 18px; color: #6b7280; }
</style>