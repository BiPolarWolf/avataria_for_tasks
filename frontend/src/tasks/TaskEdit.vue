<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { ProgressSpinner } from 'primevue'
import api from '@/client'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue'
import MyRatingInput from '@/components/inputs/MyRatingInput.vue'

// id приходит из маршрута /tasks/:id/edit (props: true в роутере).
const props = defineProps<{ id: string }>()
const router = useRouter()

const taskId = Number(props.id)

const data = reactive({
  id: taskId,
  description: '',
  complexity: 1,
  status: false,
})

// Подгружаем задачу по id и заполняем форму.
const { data: task, isPending, isError } = useQuery({
  queryKey: ['tasks', taskId],
  queryFn: async () => (await api.get(`/tasks/${taskId}`)).data,
})

watch(
  task,
  (t) => {
    if (!t) return
    data.id = t.id
    data.description = t.description
    data.complexity = t.complexity
    data.status = t.status
  },
  { immediate: true },
)

const success_function = () => {
  router.push({ name: 'tasks' })
}
</script>

<template>
  <ProgressSpinner v-if="isPending" />
  <div v-else-if="isError" class="load-error">Не удалось загрузить задачу</div>

  <MyForm
    v-else
    title="Обновить задачу"
    :data="data"
    url="tasks/update"
    :success_function="success_function"
    :mutated_keys_list="['tasks']"
    success_message="Задача обновлена"
  >
    <MyTextArea
      :is_restricted="true"
      v-model="data.description"
      label="Описание"
      placeholder="Например: пройти ежедневные задания и собрать награды"
    />

    <MyRatingInput v-model="data.complexity" label="Сложность" />
  </MyForm>
</template>
