// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/client'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  // Стейт
  const token = ref<string | null>(localStorage.getItem('accessToken'))

  const savedUser = localStorage.getItem('user')
  const user = ref<any | null>(savedUser ? JSON.parse(savedUser) : null)

  // Геттеры
  const isAuthenticated = computed(() => !!token.value)

  // Экшены
  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('accessToken', newToken)
  }

  function setUser(userData: any) {
    user.value = userData

    // Превращаем объект в JSON-строку перед сохранением
    localStorage.setItem('user', JSON.stringify(userData))

  }

   async function logout() {
    try {
        // 1. Отправляем запрос на бэкенд, чтобы FastAPI стер HttpOnly куку
        await api.post('/logout')
    } catch (error) {
        console.error("Не удалось очистить куку на сервере", error)
    } finally {
        // 2. В любом случае чистим локальный стейт фронтенда
        token.value = null
        user.value = null
        localStorage.removeItem('access_token')
        
        // 3. Кидаем юзера на страницу входа
        router.push('/login')
    }
    }
  return {
    user,
    token,
    isAuthenticated,
    setToken,
    setUser,
    logout
  }}
)