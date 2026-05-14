<script setup lang="ts">
import { useQuery} from '@tanstack/vue-query'
import MyCard from '@/components/MyCard.vue'
import MyButton from '@/components/MyButton.vue'
import { formatShortDate } from '@/utils/general'
import { ProgressSpinner} from 'primevue'
import { ref } from 'vue'
import TaskUpdateDialog from './TaskUpdateDialog.vue'
import TaskCompleteConfirmButton from './TaskCompleteConfirmButton.vue'
import TaskDeleteConfirmButton from './TaskDeleteConfirmButton.vue'
import api from '@/client'



interface Props {
  status: "active" | 'completed'
}

const props = defineProps<Props>()

const getErrorMessage = () => {
  const queryError = error.value as {
    response?: {
      data?: {
        detail?: string
      }
    }
  } | null

  return queryError?.response?.data?.detail ?? 'Не удалось загрузить задачи'
}


// Функция запроса (теперь она отделена от жизненного цикла компонента)
const fetchTasks = async () => {
  const response = await api.get(`/tasks/${props.status}`)
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
    <div v-else-if="isError" class="task_error">
      {{ getErrorMessage() }}
    </div>

    <MyCard v-else class="my-3" v-for="task in data">
        <template #content>
        <p class="task_description">{{ task.description }}</p>
        <br>
        <p >Сложность:  <img class="w-6 inline" v-for="value in task.complexity"  src="@/assets/icons/CatHead.png" alt="()"></p>
        </template>

        <template #subtitle> 
            {{ formatShortDate(task.created_at) }} {{ task.completed_at ? `- ${formatShortDate(task.completed_at)}` : "" }}
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
            <TaskDeleteConfirmButton
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

.task_description {
  white-space: pre-wrap;
}

.task_error {
  padding: 1rem;
  border: 3px solid var(--color-secondary-700);
  background: rgba(241, 226, 204, 0.92);
  color: var(--color-secondary-900);
}

</style>
