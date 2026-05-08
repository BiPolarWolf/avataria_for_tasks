<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'primevue'
import MyButton from '@/components/MyButton.vue'
import MyDialog from '@/components/MyDialog.vue'

interface Props {
  taskId: number
  taskDescription?: string
}

const props = defineProps<Props>()

const visible = ref(false)
const toast = useToast()
const queryClient = useQueryClient()

const completeTask = async () => {
  const token = localStorage.getItem('access_token')

  if (!token) {
    throw new Error('Сначала войдите в аккаунт')
  }

  const response = await axios.get(`http://localhost:8000/tasks/${props.taskId}/complete`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  })

  return response.data
}

const { mutate, isPending } = useMutation({
  mutationFn: completeTask,
  onSuccess: async () => {
    visible.value = false
    await queryClient.invalidateQueries({ queryKey: ['tasks'] })
    toast.add({
      severity: 'success',
      summary: 'Задача выполнена',
      detail: 'Она перенесена в завершённые задачи',
      life: 3000
    })
  },
  onError: (error: unknown) => {
    const detail = axios.isAxiosError(error)
      ? error.response?.data?.detail ?? 'Не удалось завершить задачу'
      : error instanceof Error
        ? error.message
        : 'Не удалось завершить задачу'

    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail,
      life: 3000
    })
  }
})

const confirmComplete = () => {
  mutate()
}
</script>

<template>
  <MyButton size="small" severity="success" @click="visible = true">
    Выполнить <i class="pi pi-check"></i>
  </MyButton>

  <MyDialog
    v-model:visible="visible"
    modal
    header="Подтвердите выполнение"
    :style="{ width: '28rem' }"
  >
    <div class="confirm_content">
      <p class="confirm_text">Отметить задачу как выполненную?</p>
      <p v-if="taskDescription" class="task_preview">{{ taskDescription }}</p>
    </div>

    <template #footer>
      <div class="confirm_actions">
        <MyButton severity="secondary" :disabled="isPending" @click="visible = false">
          Отмена
        </MyButton>
        <MyButton severity="success" :disabled="isPending" @click="confirmComplete">
          {{ isPending ? 'Сохраняем...' : 'Подтвердить' }}
        </MyButton>
      </div>
    </template>
  </MyDialog>
</template>

<style scoped>
.confirm_content {
  display: grid;
  gap: 0.75rem;
}

.confirm_text {
  margin: 0;
}

.task_preview {
  margin: 0;
  padding: 0.75rem;
  border: 2px solid var(--color-paper-700);
  background: rgba(252, 248, 243, 0.55);
  white-space: pre-wrap;
}

.confirm_actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
