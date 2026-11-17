<template>
  <div class="home-container">
    <div class="header">
      <h1>Список заявок</h1>
      <button class="btn btn-add" @click="goToAdd">
        + Добавить заявку
      </button>
    </div>

    <div class="list-container">
      <!-- Если заявок нет, показываем заглушку -->
      <div v-if="applications.length === 0" class="empty-state">
        <p>Пока нет ни одной заявки. Создайте первую завку!</p>
      </div>

      <!-- Выводим карточки в цикле -->
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import ApplicationCard from '../components/ApplicationCard.vue'

const router = useRouter()

// Имитация данных, которые в будущем придут с бэкенда
const applications = ref([
  { id: 1, number: 'РЖД-2026-001', author: 'Иванов И.И.' },
  { id: 2, number: 'РЖД-2026-002', author: 'Петров П.П.' },
  { id: 3, number: 'РЖД-2026-003', author: 'Сидоров С.С.' },
])

// Переход на страницу добавления
const goToAdd = () => {
  router.push('/add')
}

// Переход на страницу проверки (передаем ID заявки)
const verifyApplication = (id) => {
  router.push(`/verify/${id}`)
}

// Удаление заявки
const deleteApplication = (id) => {
  if (confirm('Вы уверены, что хотите удалить заявку?')) {
    applications.value = applications.value.filter(app => app.id !== id)
  }
}
</script>

<style scoped>
.home-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h1 {
  margin: 0;
  color: #111827;
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.btn-add {
  background-color: #e3000f; /* Цвет РЖД */
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-add:hover {
  background-color: #c0000c;
}

.empty-state {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 8px;
  color: #6b7280;
  border: 2px dashed #e5e7eb;
}
</style>