<template>
  <div class="add-container">
    <div class="header">
      <h1>Создание новой заявки</h1>
    </div>

    <form @submit.prevent="saveApplication" class="form-card">
      <div class="form-group">
        <label>Номер заявки</label>
        <input v-model="form.number" type="text" placeholder="Например: РЖД-2026-005" required />
      </div>

      <div class="form-group">
        <label>Автор заявки</label>
        <input v-model="form.author" type="text" placeholder="Иванов И.И." required />
      </div>

      <div class="form-group">
        <label>Номер локомотива</label>
        <input v-model="form.locoNumber" type="text" placeholder="ТЭМ2-1234" />
      </div>

      <div class="form-group">
        <label>Тип неисправности</label>
        <select v-model="form.failureType">
          <option value="Сбой ПО">Сбой ПО</option>
          <option value="Отказ датчика">Отказ датчика</option>
          <option value="Проблема с тормозами">Проблема с тормозами</option>
          <option value="Другое">Другое</option>
        </select>
      </div>

      <div class="form-group">
        <label>Описание обстоятельств</label>
        <textarea v-model="form.description" rows="4" placeholder="Подробно опишите, что произошло..."></textarea>
      </div>

      <div class="actions">
        <button type="button" class="btn btn-secondary" @click="goHome">
          На главную
        </button>
        <button type="submit" class="btn btn-primary">
          Сохранить
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Объект для хранения данных формы
const form = ref({
  number: '',
  author: '',
  locoNumber: '',
  failureType: 'Сбой ПО',
  description: ''
})

const goHome = () => {
  router.push('/')
}

const saveApplication = () => {
  // В будущем здесь будет запрос к FastAPI: POST /api/applications
  console.log('Сохранение заявки:', form.value)

  // Имитация успешного сохранения и переход на главную
  alert('Заявка успешно сохранена!')
  router.push('/')
}
</script>

<style scoped>
.add-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.header {
  margin-bottom: 30px;
}

h1 {
  color: #111827;
  margin: 0;
}

.form-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #374151;
}

input, select, textarea {
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 16px;
  font-family: inherit;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn {
  padding: 12px 24px;
  border-radius: 6px;
  border: none;
  font-size: 16px;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-primary {
  background-color: #e3000f;
  color: white;
}
.btn-primary:hover {
  background-color: #c0000c;
}

.btn-secondary {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}
.btn-secondary:hover {
  background-color: #e5e7eb;
}
</style>