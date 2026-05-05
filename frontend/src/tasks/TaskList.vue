<script setup lang="ts">
import { ref, onMounted , type Ref } from 'vue'
import axios from 'axios'
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { useToast , Button, } from 'primevue'
import TaskDetailDialog from './TaskDetailDialog.vue'

const toast = useToast()

const task_detail_visible: Ref<boolean> = ref(false)
const selected_task_id : Ref<number | null> = ref(null)





const show_task_detail = (task_id:number) => {
    task_detail_visible.value = true;
    selected_task_id.value = task_id
};

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
    <TaskDetailDialog v-model:visible="task_detail_visible"/>
    <MyCard class="my-3" v-for="task in data">
      <template #content>
      {{ task.description }}
      </template>
      
      <template #subtitle> 
        {{ formatShortDate(task.created_at) }}
      </template>

      <template #buttons>

      <Button v-on:click="show_task_detail(task.id)" size="small" severity="contrast">
          Опции <i class="pi pi-cog"></i>
        </Button>
      </template>

    </MyCard>

    <p v-if="message">{{ message }}</p>


</template>
