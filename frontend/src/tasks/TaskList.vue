<script setup lang="ts">
import { ref, onMounted , type Ref } from 'vue'
import axios from 'axios'

const data: Ref<any[]> = ref([])
const message = ref('')

onMounted(async () => {
  try {
    // Пока указываем прямой URL, позже мы это оптимизируем
    const token = localStorage.getItem('access_token')

    // 2. Передаем токен в заголовки запроса
    const response = await axios.get('http://localhost:8000/tasks/', {
      headers: {
        'Authorization': `Bearer ${token}` // Формат, который ждет FastAPI
      }
    })

    data.value = response.data
  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    message.value = "Ошибка связи с бэкендом"
  }
})
</script>

<template>
    
  <div style="text-align: center;">

    <p class="border-2 mb-1" v-for="value in data">
        {{ value.description }}
    </p>

    <p v-if="message">{{ message }}</p>

  </div>
  

</template>
