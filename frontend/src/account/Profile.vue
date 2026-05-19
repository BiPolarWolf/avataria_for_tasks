<script setup lang="ts">

import { onMounted, ref, type Ref } from 'vue';
import api from '@/client';

// Удобнее инициализировать null для объекта пользователя
const user : Ref<any> = ref(null) 

const task_stats : Ref<any> = ref(null)

onMounted(async () => {
  try {
    // 2. Передаем токен в заголовки запроса
    const user_response = await api.get('/users/me')
    user.value = user_response.data

    const user_stats_response = await api.get('/tasks/stats')
    task_stats.value = user_stats_response.data


  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    // Здесь можно добавить логику редиректа на страницу логина, 
    // если сервер вернул ошибку 401 (Unauthorized)
  }
})

</script>

<template>

<div v-if="user" class="m-5">
<h1 class="text-xl text-white"> Пользователь </h1>
<p class="text-amber-300"><span class="bold">Имя : </span>{{ user.username }}</p>
<p class="text-amber-300"><span class="bold">Email : </span>{{ user.email }}</p>
</div>


<div v-if="task_stats" class="m-5">
<h1 class="text-xl text-white">Статистика задач </h1>
<p class="text-amber-500"><span class="bold">В процессе : </span>{{ task_stats.false }}</p>
<p class="text-amber-500"><span class="bold">Завершенные : </span>{{ task_stats.true }}</p>
</div>

</template>