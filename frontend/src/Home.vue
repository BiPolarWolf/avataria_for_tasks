
<script setup>
import { ref, onMounted } from 'vue'
import api from '@/client'

const message = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/')
    message.value = response.data.hello_world
  } catch (error) {
    console.error("Ошибка при получении данных:", error)
    message.value = "Ошибка связи с бэкендом"
  }
})
</script>

<template>
    
  <div style="text-align: center;">

    <p>{{ message }}</p>


  </div>
  

</template>
