<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'primevue/usetoast'

import api from '@/client'
import MyButton from '@/components/MyButton.vue'
import MyDialog from '@/components/MyDialog.vue'

interface Props {
  tagId: number
  tagText?: string
}

const props = defineProps<Props>()

const visible = ref(false)
const toast = useToast()
const queryClient = useQueryClient()

const untieTag = async () => {
  const response = await api.post(`/tags/${props.tagId}/untie`)
  return response.data
}

const { mutate, isPending } = useMutation({
  mutationFn: untieTag,
  onSuccess: async () => {
    visible.value = false

    await Promise.all([
      queryClient.invalidateQueries({ queryKey: ['tags'] }),
      queryClient.invalidateQueries({ queryKey: ['notes'] }),
    ])

    toast.add({
      severity: 'success',
      summary: 'Тег отвязан',
      detail: 'Записи обновятся без этого тега',
      life: 3000,
    })
  },
  onError: (error: unknown) => {
    const detail = axios.isAxiosError(error)
      ? error.response?.data?.detail ?? 'Не удалось отвязать тег'
      : error instanceof Error
        ? error.message
        : 'Не удалось отвязать тег'

    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail,
      life: 3000,
    })
  },
})

const confirmUntie = () => {
  mutate()
}
</script>

<template>
  <MyButton type="button" severity="warning" :disabled="isPending || !tagId" @click="visible = true">
    Отвязать
  </MyButton>

  <MyDialog
    v-model:visible="visible"
    modal
    header="Отвязать тег"
    :style="{ width: '30rem' }"
  >
    <div class="confirm_content">
      <p class="confirm_text">Отвязать этот тег от всех записей?</p>
      <p v-if="tagText" class="object_preview">{{ tagText }}</p>
      <p class="hint_text">Сам тег не удалится, но исчезнет из уже привязанных записей.</p>
    </div>

    <template #footer>
      <div class="confirm_actions">
        <MyButton severity="secondary" :disabled="isPending" @click="visible = false">
          Отмена
        </MyButton>
        <MyButton severity="warning" :disabled="isPending" @click="confirmUntie">
          {{ isPending ? 'Отвязываем...' : 'Отвязать' }}
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

.confirm_text,
.hint_text {
  margin: 0;
}

.hint_text {
  color: var(--color-secondary-800);
  font-size: 0.9rem;
}

.object_preview {
  margin: 0;
  padding: 0.75rem;
  border: 2px solid var(--color-paper-700);
  background: rgba(252, 248, 243, 0.55);
}

.confirm_actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>
