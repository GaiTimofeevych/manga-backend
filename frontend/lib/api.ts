import axios from 'axios';
import { getToken } from './auth';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor (Перехватчик): срабатывает ПЕРЕД каждым запросом
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    // Если токен есть - добавляем его в заголовок Authorization
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;