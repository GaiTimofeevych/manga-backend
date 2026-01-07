import axios from 'axios';

// Создаем экземпляр (instance) axios с базовыми настройками
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // Базовый URL твоего API
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;