<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { useToast } from 'primevue'
import MyButton from '@/components/MyButton.vue'
import MyDialog from '@/components/MyDialog.vue'
import api from '@/client'


interface Props {
    description?: string
    queryKey : string
    object_id : number
}

const props = defineProps<Props>()

const visible = ref(false)
const toast = useToast()
const queryClient = useQueryClient()

const deleteFunc = async () => {
  const response = await api.delete(`/${props.queryKey}/${props.object_id}`)

  return response.data
}

const { mutate, isPending } = useMutation({
  mutationFn: deleteFunc,
  onSuccess: async () => {
    visible.value = false
    await queryClient.invalidateQueries({ queryKey: [props.queryKey] })
    toast.add({
      severity: 'success',
      summary: `Объект удален`,
      detail: `Он больше не отображается в списке `,
      life: 3000
    })
  },
  onError: (error: unknown) => {
    const detail = axios.isAxiosError(error)
      ? error.response?.data?.detail ?? 'Не удалось удалить объект'
      : error instanceof Error
        ? error.message
        : 'Не удалось удалить объект'

    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail,
      life: 3000
    })
  }
})

const confirmDelete = () => {
  mutate()
}
</script>

<template>
  <MyButton size="small" severity="danger" @click="visible = true">
    Удалить <img src="@/assets/icons/Trashbin.png" width="18" alt="">
  </MyButton>

  <MyDialog
    v-model:visible="visible"
    modal
    header="Подтвердите удаление"
    :style="{ width: '28rem' }"
  >
    <div class="confirm_content">
      <p class="confirm_text">Удалить без возможности восстановления?</p>
      <p v-if="description" class="object_preview">{{ description }}</p>
    </div>

    <template #footer>
      <div class="confirm_actions">
        <MyButton severity="secondary" :disabled="isPending" @click="visible = false">
          Отмена
        </MyButton>
        <MyButton severity="danger" :disabled="isPending" @click="confirmDelete">
          {{ isPending ? 'Удаляем...' : 'Удалить' }}
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

.object_preview {
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