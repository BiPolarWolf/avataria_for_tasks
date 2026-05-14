import axios from 'axios';
import router from './router/index'; // Импортируй свой экземпляр роутера

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// Добавляем интерцептор ответов
api.interceptors.response.use(
  (response) => {
    // Если запрос прошел успешно, просто возвращаем ответ
    return response;
  },
  (error) => {
    // Проверяем, что ошибка именно 401 (Unauthorized)
    if (error.response && error.response.status === 401) {
      
      // 1. Очищаем локальное хранилище (токен, данные пользователя)
      localStorage.removeItem('access_token');
      
      // 2. Делаем редирект на страницу логина
      // Проверяем, чтобы не редиректить бесконечно, если мы уже на странице логина
      if (router.currentRoute.value.name !== 'login') {
        router.push({ name: 'login' });
      }
    }

    return Promise.reject(error);
  }
);

export default api;
