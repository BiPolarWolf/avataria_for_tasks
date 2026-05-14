
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/client'

const message = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/about')
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
