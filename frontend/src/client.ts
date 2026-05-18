import axios from 'axios';
import router from './router/index'; // Импортируй свой экземпляр роутера

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials : true
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
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // 1. КРИТИЧЕСКИ ВАЖНО: Если сам запрос /refresh упал с 401, 
    // или мы уже пробовали повторить запрос, ничего не делаем — сразу в отказ.
    if (originalRequest.url?.includes('/refresh') || originalRequest._isRetry) {
      return Promise.reject(error);
    }

    // Проверяем, что ошибка 401
    if (error.response && error.response.status === 401) {
      originalRequest._isRetry = true;

      try {
        // 2. Пытаемся обновить токен
        const response = await api.post('/refresh');
        const newAccessToken = response.data.access_token;

        // 3. Сохраняем новый токен
        localStorage.setItem('access_token', newAccessToken);

        // 4. Обновляем заголовок и повторяем оригинальный запрос
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        return api(originalRequest);
        
      } catch (refreshError) {
        // Если рефреш не сработал (токен протух, удален на сервере и т.д.)
        // Просто чистим локальные данные и жестко редиректим на логин
        localStorage.removeItem('access_token');
        
        // Перенаправление на логин
        if (router.currentRoute.value.name !== 'login') {
          router.push({ name: 'login' });
        }
        
        // Обязательно возвращаем отклоненный промис, чтобы прервать цепочку
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
