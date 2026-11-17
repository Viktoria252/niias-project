<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router' // Добавили useRoute и useRouter

const route = useRoute()
const router = useRouter()

// Получаем ID из URL (например, /verify/1)
const applicationId = ref(route.params.id || 'Неизвестно')

const isAnalyzing = ref(false)
const showResults = ref(false)

const fields = ref([
  // ... (оставьте ваш массив fields как был) ...
  { id: 'loco', label: 'Номер локомотива', value: 'ТЭМ2-1234', aiValue: 'ТЭМ2-1234', status: 'pending' },
  { id: 'station', label: 'Станция', value: 'Москва-Сорт', aiValue: 'Москва-Пасс', status: 'pending' },
])

const hasErrors = computed(() => fields.value.some(f => f.status === 'error'))

const goHome = () => {
  router.push('/') // Теперь используем router вместо alert
}

const saveApplication = () => {
  alert('Заявка сохранена!')
  router.push('/')
}

// ... (остальные методы handleFileUpload, replaceField, replaceAll остаются без изменений) ...
</script>