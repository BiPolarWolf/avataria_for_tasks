<script setup lang="ts">
import { useQuery} from '@tanstack/vue-query'
import axios from 'axios'
import MyCard from '@/components/MyCard.vue'
import MyButton from '@/components/MyButton.vue'
import { formatShortDate } from '@/utils/general'
import { useToast , ProgressSpinner} from 'primevue'
import { ref } from 'vue'
import TaskUpdateDialog from './TaskUpdateDialog.vue'
import TaskCompleteConfirmButton from './TaskCompleteConfirmButton.vue'



interface Props {
  status: "active" | 'completed'
}

const props = defineProps<Props>()

const toast = useToast()



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

const selected_task = ref(null)
const visible = ref(false)

const update_task = (task:any) => {
  visible.value = true
  selected_task.value = task
};


</script>



<template>

    <TaskUpdateDialog v-model:visible="visible" v-model:initial="selected_task" />

    <template v-if="isPending">
       <ProgressSpinner />
    </template>

    <MyCard v-else class="my-3" v-for="task in data">
        <template #content>
        <p>{{ task.description }} </p>
        <br>
        <p >Сложность:  <img class="w-6 inline" v-for="value in task.complexity"  src="@/assets/icons/CatHead.png" alt="()"></p>
        </template>

        <template #subtitle> 
            {{ formatShortDate(task.created_at) }}
        </template>


        <template #buttons> <span></span></template>

        <template #footer>
          <div class="task_actions">
            <MyButton
            v-if="props.status === 'active'"
            size="small" severity="info" v-on:click="() =>update_task(task)"  class="detail_button">
                Изменить  <img src="@/assets/icons/Wrench.png" style="width: 18px;" alt="">
            </MyButton>
            <TaskCompleteConfirmButton
              v-if="props.status === 'active'"
              :task-id="task.id"
              :task-description="task.description"
            />
          </div>
        </template>

    </MyCard>

</template>

<style scoped>

.detail_button{
  background-color: var(--color-secondary-500);
  border: 4px solid var(--color-secondary-800);
  color: white;
}

.task_actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

</style>
