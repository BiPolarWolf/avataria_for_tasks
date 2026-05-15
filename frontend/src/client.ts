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

    // Проверяем, что ошибка 401 и мы еще не пробовали повторить этот запрос
    if (error.response && error.response.status === 401 && !originalRequest._isRetry) {
      originalRequest._isRetry = true;

      try {
        // 1. Пытаемся обновить access_token
        // Кука refresh_token подставится браузером автоматически (withCredentials: true)
        const response = await api.post('/refresh');
        
        const newAccessToken = response.data.access_token;

        // 2. Сохраняем новый токен
        localStorage.setItem('access_token', newAccessToken);

        // 3. Обновляем заголовок в оригинальном запросе
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

        // 4. Повторяем оригинальный запрос с новым токеном
        return api(originalRequest);
      } catch (refreshError) {
        // Если даже /refresh выдал 401 (рефреш-токен протух)
        console.error("Refresh token expired. Logging out...");
        
        localStorage.removeItem('access_token');
        if (router.currentRoute.value.name !== 'login') {
          router.push({ name: 'login' });
        }
      }
    }

    return Promise.reject(error);
  }
);

export default api;
