
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const message = ref('')

onMounted(async () => {
  try {
    // Пока указываем прямой URL, позже мы это оптимизируем
    const response = await axios.get('http://localhost:8000/about')
    message.value = response.data
  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    message.value = "Ошибка связи с бэкендом"
  }
})
</script>

<template>
    
  <div style="text-align: center;">

    <h1 class="text-3xl">{{ message.title }}</h1>

    <p>{{ message.description }}</p>

  </div>
  

</template>
