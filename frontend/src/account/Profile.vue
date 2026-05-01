<script setup lang="ts">
import axios from 'axios';
import { onMounted, ref } from 'vue';

// Удобнее инициализировать null для объекта пользователя
const user = ref(null) 

onMounted(async () => {
  try {
    // 1. Достаем токен из хранилища
    const token = localStorage.getItem('access_token')

    // 2. Передаем токен в заголовки запроса
    const response = await axios.get('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}` // Формат, который ждет FastAPI
      }
    })
    
    user.value = response.data
  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    // Здесь можно добавить логику редиректа на страницу логина, 
    // если сервер вернул ошибку 401 (Unauthorized)
  }
})

</script>

<template>
<h1 cla>Страница Профиля</h1>

<p class="text-amber-300">{{ user }}</p>

</template>