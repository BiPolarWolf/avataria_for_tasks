<script lang="ts" setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'primevue'
import MyButton from '@/components/MyButton.vue'

interface TaskCreatePayload {
  description: string
  complexity: number
}

const toast = useToast()
const queryClient = useQueryClient()

const formData = reactive<TaskCreatePayload>({
  description: '',
  complexity: 1,
})

const resetForm = () => {
  formData.description = ''
  formData.complexity = 1
}

const createTask = async (payload: TaskCreatePayload) => {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('Сначала войдите в аккаунт')
  }

  const response = await axios.post('http://localhost:8000/tasks/create', payload, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  return response.data
}

const { mutate, isPending } = useMutation({
  mutationFn: createTask,
  onSuccess: async () => {
    resetForm()
    await queryClient.invalidateQueries({ queryKey: ['tasks'] })
    toast.add({
      severity: 'success',
      summary: 'Задача создана',
      detail: 'Теперь она должна появиться во вкладке активных задач',
      life: 3000
    })
  },
  onError: (error: unknown) => {
    const detail = axios.isAxiosError(error)
      ? error.response?.data?.detail ?? 'Не удалось создать задачу'
      : error instanceof Error
        ? error.message
        : 'Не удалось создать задачу'

    toast.add({
      severity: 'error',
      summary: 'Ошибка создания',
      detail,
      life: 3000
    })
  }
})

const submitForm = () => {
  mutate({
    description: formData.description,
    complexity: Number(formData.complexity),
  })
}
</script>

<template>
  <form class="task_form" @submit.prevent="submitForm">
    <div class="field">
      <label class="field_label" for="task_description">Описание задачи</label>
      <textarea
        id="task_description"
        v-model="formData.description"
        class="field_control textarea"
        name="description"
        rows="5"
        maxlength="500"
        placeholder="Например: пройти ежедневные задания и собрать награды"
        required
      />
    </div>

    <div class="field">
      <label class="field_label" for="task_complexity">
        Сложность: {{ formData.complexity }}
      </label>
      <input
        id="task_complexity"
        v-model="formData.complexity"
        class="range_control"
        type="range"
        min="1"
        max="5"
        step="1"
      >
      <div class="range_labels">
        <span>1</span>
        <span>5</span>
      </div>
    </div>

    <div class="actions">
      <MyButton type="submit" :disabled="isPending || !formData.description.trim()" severity="contrast">
        {{ isPending ? 'Создаём...' : 'Создать задачу' }}
      </MyButton>
    </div>
  </form>
</template>

<style scoped>
.task_form {
  max-width: 720px;
  margin: 0 auto;
  padding: 24px;
  border: 4px solid var(--color-primary-400);
  background: rgba(246, 214, 189, 0.96);
  color: #373737;
  display: grid;
  gap: 20px;
  box-shadow: 8px 8px 0 rgba(15, 43, 64, 0.35);
}

.field {
  display: grid;
  gap: 8px;
}

.field_label {
  font-family: 'PixeloidSans', sans-serif;
  font-size: 14px;
  color: var(--color-secondary-800);
}

.field_control {
  width: 100%;
  padding: 12px;
  border: 3px solid var(--color-secondary-600);
  background: #fff8f3;
  color: #2c2c2c;
  resize: vertical;
  outline: none;
}

.field_control:focus {
  border-color: var(--color-primary-600);
}

.textarea {
  min-height: 140px;
}

.range_control {
  width: 100%;
  accent-color: var(--color-primary-700);
}

.range_labels {
  display: flex;
  justify-content: space-between;
  color: var(--color-secondary-700);
  font-size: 14px;
}

.actions {
  display: flex;
  justify-content: flex-end;
}
</style>
