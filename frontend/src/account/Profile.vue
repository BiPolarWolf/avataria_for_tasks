<script setup lang="ts">

import { onMounted, ref } from 'vue';
import api from '@/client';

// Удобнее инициализировать null для объекта пользователя
const user = ref(null) 

onMounted(async () => {
  try {
    // 1. Достаем токен из хранилища
    const token = localStorage.getItem('access_token')

    // 2. Передаем токен в заголовки запроса
    const response = await api.get('/users/me')
    
    user.value = response.data
  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    // Здесь можно добавить логику редиректа на страницу логина, 
    // если сервер вернул ошибку 401 (Unauthorized)
  }
})

</script>

<template>
<h1 class="text-xl">Страница Профиля 1</h1>

<p class="text-amber-300">{{ user }}</p>

</template>