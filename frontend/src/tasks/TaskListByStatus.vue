<script setup lang="ts">
import { useQuery} from '@tanstack/vue-query'
import axios from 'axios'
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { useToast , Button ,ProgressSpinner, Image} from 'primevue'


interface Props {
  status: "active" | 'completed'
}

const props = defineProps<Props>()

const toast = useToast()

const complete_task = () => {
    toast.add({ severity: 'info', summary: 'Не имплементировано', detail: 'Вы должны заменить Кнопку на свою', life: 3000 });
};

// Функция запроса (теперь она отделена от жизненного цикла компонента)
const fetchTasks = async () => {
  const token = localStorage.getItem('access_token')
  const response = await axios.get(`http://localhost:8000/tasks/${props.status}`,{
    headers: {
      Authorization: `Bearer ${token}`
    }
  })
  return response.data
}

// Основной хук Vue Query
const {isPending, isFetching, isError, data, error } = useQuery({
  queryKey: ['tasks', props.status], // Разделяем кэш по статусу задач
  queryFn: fetchTasks, // Сама функция запроса
  retry: 1,            // Количество попыток при ошибке
})
</script>

<template>

    <template v-if="isPending">
       <ProgressSpinner />
    </template>

    <MyCard v-else class="my-3" v-for="task in data">
        <template #content>
        <p>{{ task.description }} </p>
        <p><i v-for="value in task.complexity" class="pi pi-star"></i> </p>
        </template>

        
        <template #subtitle> 
            {{ formatShortDate(task.created_at) }}
        </template>

        <template #buttons>

        <Button v-on:click="complete_task" size="small" class="detail_button">
            Детали <i class="pi pi-file"></i>
            </Button>
        </template>

    </MyCard>

</template>

<style scoped>

.detail_button{
  background-color: var(--color-secondary-500);
  border: 4px solid var(--color-secondary-800);
  color: white;
}

</style>
