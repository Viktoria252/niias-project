const API_BASE = '/api';

export const api = {
  // Получить все заявки
  async getApplications() {
    const response = await fetch(`${API_BASE}/applications`);
    if (!response.ok) throw new Error('Ошибка загрузки заявок');
    return await response.json();
  },

  // Создать заявку
  async createApplication(data) {
    const response = await fetch(`${API_BASE}/applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Ошибка создания заявки');
    return await response.json();
  },

  // Удалить заявку
  async deleteApplication(id) {
    const response = await fetch(`${API_BASE}/applications/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Ошибка удаления');
    return await response.json();
  }

  // Получить одну заявку
  async getApplicationById(id) {
    const response = await fetch(`${API_BASE}/applications/${id}`);
    if (!response.ok) throw new Error('Ошибка загрузки заявки');
    return await response.json();
  },

  // Обновить заявку
  async updateApplication(id, data) {
    const response = await fetch(`${API_BASE}/applications/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    if (!response.ok) throw new Error('Ошибка обновления заявки');
    return await response.json();
  },

  // Отправить на анализ ИИ
  async analyzeDocument(id) {
    const response = await fetch(`${API_BASE}/analyze/${id}`, {
      method: 'POST'
    });
    if (!response.ok) throw new Error('Ошибка анализа');
    return await response.json();
  }
};