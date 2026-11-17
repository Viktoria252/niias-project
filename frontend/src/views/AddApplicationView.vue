import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../services/api' // <--- Импортируем API

const router = useRouter()

const form = ref({
  number: '',
  author: '',
  loco_number: '',
  failure_type: 'Сбой ПО',
  description: ''
})

const goHome = () => router.push('/')

const saveApplication = async () => {
  try {
    await api.createApplication(form.value) // <--- Отправляем POST запрос
    alert('Заявка успешно сохранена!')
    router.push('/') // Возвращаемся на главную
  } catch (error) {
    console.error(error)
    alert('Ошибка при сохранении заявки')
  }
}