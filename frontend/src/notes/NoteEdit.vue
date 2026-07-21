<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { ProgressSpinner } from 'primevue'
import api from '@/client'
import MyForm from '@/components/MyForm.vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue'
import MyRatingInput from '@/components/inputs/MyRatingInput.vue'
import MySelect from '@/components/inputs/MySelect.vue'

// id приходит из маршрута /notes/:id/edit (props: true в роутере).
const props = defineProps<{ id: string }>()
const router = useRouter()

const noteId = Number(props.id)
const tagsApiUrl = 'tags/'

const data = reactive({
  id: noteId,
  title: '',
  text: '',
  importans: 1,
  tag_ids: [] as number[],
})

// Подгружаем запись по id и заполняем форму.
const { data: note, isPending, isError } = useQuery({
  queryKey: ['notes', noteId],
  queryFn: async () => (await api.get(`/notes/${noteId}`)).data,
})

watch(
  note,
  (n) => {
    if (!n) return
    data.id = n.id
    data.title = n.title
    data.text = n.text
    data.importans = n.importans
    data.tag_ids = n.tags.map((tag: { id: number }) => tag.id)
  },
  { immediate: true },
)

const success_function = () => {
  router.push({ name: 'notes' })
}
</script>

<template>
  <ProgressSpinner v-if="isPending" />
  <div v-else-if="isError" class="load-error">Не удалось загрузить запись</div>

  <MyForm
    v-else
    title="Обновить запись"
    :data="data"
    url="notes/update"
    :success_function="success_function"
    :mutated_keys_list="['notes']"
    success_message="Запись обновлена"
  >
    <MyTextInput v-model="data.title" label="Заголовок" />

    <MyTextArea
      :is_restricted="true"
      v-model="data.text"
      label="Описание"
      placeholder="Например: как прошел мой день"
    />

    <MyRatingInput v-model="data.importans" :max="10" label="Важность" />

    <MySelect
      option-label="text"
      option-value="id"
      v-model="data.tag_ids"
      multiple
      :api-url="tagsApiUrl"
      label="Теги"
    />
  </MyForm>
</template>
