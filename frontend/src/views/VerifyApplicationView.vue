<template>
  <div class="verify-container" v-if="application">
    <!-- Шапка -->
    <div class="header-actions">
      <button class="btn btn-secondary" @click="goHome">← На главную</button>
      <h2>Проверка заявки № {{ application.number }}</h2>
      <button class="btn btn-primary" @click="saveChanges">Сохранить</button>
    </div>

    <!-- Зона загрузки файлов -->
    <div class="upload-section" :class="{ 'analyzing': isAnalyzing }">
      <div v-if="!isAnalyzing" class="drop-zone">
        <p>Перетащите сюда PDF или фото бланка для проверки ИИ</p>
        <input type="file" ref="fileInput" @change="handleFileUpload" hidden />
        <button class="btn btn-outline" @click="$refs.fileInput.click()">Выбрать файл</button>
      </div>
      <div v-else class="spinner-container">
        <div class="spinner"></div>
        <p>ИИ анализирует документ...</p>
      </div>
    </div>

    <!-- Панель результатов -->
    <div v-if="showResults" class="results-panel">
      <div class="status-info">
        <span v-if="hasErrors" class="text-error">Обнаружены расхождения</span>
        <span v-else class="text-success">Все данные совпадают</span>
      </div>
      <button v-if="hasErrors" class="btn btn-warning" @click="replaceAll">
        Заменить все значения
      </button>
    </div>

    <!-- Умная форма -->
    <div class="form-grid">
      <div v-for="(field, index) in fields" :key="field.key" class="form-group" :class="field.status">
        <label>{{ field.label }}</label>

        <div class="input-wrapper">
          <input
            v-model="field.value"
            :class="{ 'input-error': field.status === 'error', 'input-success': field.status === 'success' }"
          />
          <span v-if="field.status === 'success'" class="icon-success">✓</span>
          <span v-if="field.status === 'error'" class="icon-error">⚠️</span>
        </div>

        <!-- Подсказка -->
        <div v-if="field.status === 'error'" class="suggestion-box">
          <p>ИИ предлагает: <strong>{{ field.aiValue }}</strong></p>
          <button class="btn btn-small btn-outline" @click="replaceField(index)">Заменить</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="loading">Загрузка данных заявки...</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../services/api'

const route = useRoute()
const router = useRouter()
const appId = route.params.id

const application = ref(null)
const isAnalyzing = ref(false)
const showResults = ref(false)

// Структура полей для формы
const fields = ref([
  { key: 'loco_number', label: 'Номер локомотива', value: '', aiValue: '', status: 'pending' },
  { key: 'failure_type', label: 'Тип неисправности', value: '', aiValue: '', status: 'pending' },
  { key: 'description', label: 'Описание', value: '', aiValue: '', status: 'pending' },
])

const hasErrors = computed(() => fields.value.some(f => f.status === 'error'))

// Загружаем заявку при старте
onMounted(async () => {
  try {
    const data = await api.getApplicationById(appId)
    application.value = data
    // Заполняем форму реальными данными
    fields.value.forEach(f => {
      f.value = data[f.key] || ''
    })
  } catch (error) {
    alert('Ошибка загрузки заявки')
    router.push('/')
  }
})

const goHome = () => router.push('/')

// Сохранение изменений в БД
const saveChanges = async () => {
  try {
    const updatedData = { ...application.value }
    fields.value.forEach(f => {
      updatedData[f.key] = f.value
    })
    await api.updateApplication(appId, updatedData)
    alert('Заявка успешно обновлена!')
    router.push('/')
  } catch (error) {
    alert('Ошибка при сохранении')
  }
}

// Имитация загрузки файла и анализа
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  isAnalyzing.value = true
  showResults.value = false

  try {
    // Отправляем запрос на бэкенд
    const result = await api.analyzeDocument(appId)
    const aiData = result.ai_data

    // Сравниваем данные
    fields.value.forEach(field => {
      field.aiValue = aiData[field.key] || ''
      if (field.value === field.aiValue) {
        field.status = 'success'
      } else {
        field.status = 'error'
      }
    })
    showResults.value = true
  } catch (error) {
    alert('Ошибка при анализе документа')
  } finally {
    isAnalyzing.value = false
  }
}

const replaceField = (index) => {
  const field = fields.value[index]
  field.value = field.aiValue
  field.status = 'success'
}

const replaceAll = () => {
  fields.value.forEach(field => {
    if (field.status === 'error') {
      field.value = field.aiValue
      field.status = 'success'
    }
  })
}
</script>

<style scoped>
/* Стили оставляем точно такими же, как были в прошлом шаге */
.verify-container { max-width: 900px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
.header-actions { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #eee; }
h2 { margin: 0; color: #333; }
.upload-section { background: #f8f9fa; border: 2px dashed #cbd5e1; border-radius: 8px; padding: 40px; text-align: center; margin-bottom: 20px; transition: all 0.3s ease; }
.upload-section.analyzing { border-color: #3b82f6; background: #eff6ff; }
.drop-zone p { color: #64748b; margin-bottom: 15px; }
.spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3b82f6; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.results-panel { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }
.status-info { font-weight: bold; }
.text-error { color: #dc2626; }
.text-success { color: #059669; }
.form-grid { display: flex; flex-direction: column; gap: 20px; }
.form-group { display: flex; flex-direction: column; transition: all 0.3s ease; }
.form-group label { font-weight: bold; margin-bottom: 8px; color: #374151; }
.input-wrapper { position: relative; }
input { width: 100%; padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 16px; transition: border-color 0.3s, box-shadow 0.3s; box-sizing: border-box; }
.input-error { border-color: #ef4444 !important; background-color: #fef2f2; padding-right: 40px; }
.input-success { border-color: #10b981 !important; background-color: #f0fdf4; padding-right: 40px; }
.icon-success { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: #10b981; font-size: 20px; font-weight: bold; }
.icon-error { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); font-size: 18px; }
.suggestion-box { background: #fffbeb; border: 1px solid #fcd34d; border-radius: 6px; padding: 10px 15px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 14px; }
.suggestion-box p { margin: 0; color: #92400e; }
.btn { padding: 10px 20px; border-radius: 6px; border: none; font-size: 15px; cursor: pointer; transition: background 0.2s, transform 0.1s; }
.btn:active { transform: scale(0.98); }
.btn-primary { background: #3b82f6; color: white; }
.btn-primary:hover { background: #2563eb; }
.btn-secondary { background: #e5e7eb; color: #374151; }
.btn-secondary:hover { background: #d1d5db; }
.btn-warning { background: #f59e0b; color: white; font-weight: bold; }
.btn-warning:hover { background: #d97706; }
.btn-outline { background: transparent; border: 1px solid #9ca3af; color: #4b5563; }
.btn-outline:hover { background: #f3f4f6; }
.btn-small { padding: 6px 12px; font-size: 13px; background: white; border: 1px solid #d97706; color: #d97706; font-weight: bold; }
.btn-small:hover { background: #fef3c7; }
.loading { text-align: center; padding: 50px; font-size: 18px; color: #6b7280; }
</style>