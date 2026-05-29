<script setup lang="ts">
import { useQuery} from '@tanstack/vue-query'
import MyCard from '@/components/MyCard.vue'
import MyButton from '@/components/MyButton.vue'
import { formatShortDate } from '@/utils/general'
import { ProgressSpinner} from 'primevue'
import { ref } from 'vue'

import api from '@/client'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'



const getErrorMessage = () => {
  const queryError = error.value as {
    response?: {
      data?: {
        detail?: string
      }
    }
  } | null

  return queryError?.response?.data?.detail ?? 'Не удалось загрузить записи'
}


// Функция запроса (теперь она отделена от жизненного цикла компонента)
const fetchNotes = async () => {
  const response = await api.get(`/notes/`)
  return response.data
}

// Основной хук Vue Query
const {isPending, isFetching, isError, data, error } = useQuery({
  queryKey: ['notes'], // Разделяем кэш по статусу задач
  queryFn: fetchNotes, // Сама функция запроса
  retry: 1,            // Количество попыток при ошибке
})

const selected_task = ref(null)
const visible = ref(false)

const update_note = (task:any) => {
  visible.value = true
  selected_task.value = task
};


</script>



<template>

    <template v-if="isPending">
       <ProgressSpinner />
    </template>
    <div v-else-if="isError" class="task_error">
      {{ getErrorMessage() }}
    </div>

    <MyCard v-else class="my-3" v-for="note in data">

        <template #content>
        <p class="task_description">{{ note.text }}</p>
        <br>
        <p >Важность:  <img class="w-6 inline" v-for="value in note.importans"  src="@/assets/icons/CatHead.png" alt="()"></p>
        </template>

        <template #subtitle> 
         {{ note.title}}    {{ formatShortDate(note.date_create) }}, {{ formatShortDate(note.date_update) }}
        </template>


        <template #buttons>
          <span></span>
        </template>

        <template #actions>
          <DeleteConfirmButton
            :object_id="note.id"
            query-key="notes"
            :description="note.text"
          />
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