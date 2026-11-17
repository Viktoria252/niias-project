<template>
  <div class="card">
    <div class="card-info">
      <h3>Заявка № {{ application.number }}</h3>
      <p class="author">Автор: {{ application.author }}</p>
    </div>
    <div class="card-actions">
      <button class="btn btn-verify" @click="$emit('verify', application.id)">
        Проверить
      </button>
      <button class="btn btn-delete" @click="$emit('delete', application.id)">
        Удалить
      </button>
    </div>
  </div>
</template>

<script setup>
// Определяем, какие данные компонент ожидает получить от родителя
defineProps({
  application: {
    type: Object,
    required: true
  }
})

// Определяем события, которые компонент может отправить наверх
defineEmits(['verify', 'delete'])
</script>

<style scoped>
.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  border-left: 4px solid #3b82f6;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.card-info h3 {
  margin: 0 0 8px 0;
  color: #1f2937;
}

.author {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.card-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  font-size: 14px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-verify {
  background-color: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
}
.btn-verify:hover {
  background-color: #e5e7eb;
}

.btn-delete {
  background-color: #fee2e2;
  color: #dc2626;
}
.btn-delete:hover {
  background-color: #fecaca;
}
</style>