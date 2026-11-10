<template>
  <div class="container">
    <h1>Ассистент диспетчера РЖД</h1>
    <div class="chat-box">
      <div v-if="answer" class="response">
        <h3>Рекомендация:</h3>
        <p>{{ answer }}</p>
      </div>
      <div v-if="sources.length" class="sources">
        <h4>Источники из базы знаний:</h4>
        <ul>
          <li v-for="(source, index) in sources" :key="index">{{ source }}</li>
        </ul>
      </div>
    </div>
    <div class="input-area">
      <input
        v-model="query"
        @keyup.enter="ask"
        placeholder="Опишите неисправность..."
        :disabled="loading"
      />
      <button @click="ask" :disabled="loading">
        {{ loading ? 'Думаю...' : 'Спросить' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const answer = ref('')
const sources = ref([])
const loading = ref(false)

const ask = async () => {
  if (!query.value) return

  loading.value = true
  answer.value = ''
  sources.value = []

  try {
    const response = await fetch('/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value })
    })

    if (!response.ok) throw new Error('Ошибка сервера')

    const data = await response.json()
    answer.value = data.answer
    sources.value = data.sources || []
  } catch (error) {
    answer.value = 'Произошла ошибка при получении ответа. Проверьте подключение.'
  } finally {
    loading.value = false
  }
}
</script>

<style>
body { font-family: sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
.container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.chat-box { min-height: 200px; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 4px; background: #fafafa; }
.input-area { display: flex; gap: 10px; }
input { flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 10px 20px; background-color: #e3000f; color: white; border: none; border-radius: 4px; cursor: pointer; } /* Цвет РЖД */
button:disabled { background-color: #999; }
.sources { margin-top: 15px; font-size: 0.9em; color: #666; }
</style>