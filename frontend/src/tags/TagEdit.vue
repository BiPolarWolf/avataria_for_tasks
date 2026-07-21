<script lang="ts" setup>
import { reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { ProgressSpinner } from 'primevue'
import api from '@/client'
import MyForm from '@/components/MyForm.vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue'
import MyColorPicker from '@/components/inputs/MyColorPicker.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'
import TagUntieButton from './TagUntieButton.vue'

// id приходит из маршрута /tags/:id/edit (props: true в роутере).
const props = defineProps<{ id: string }>()
const router = useRouter()

const tagId = Number(props.id)

const data = reactive({
  id: tagId,
  text: '',
  color: '#EAD7BB',
})

// Подгружаем тег по id и заполняем форму.
const { data: tag, isPending, isError } = useQuery({
  queryKey: ['tags', tagId],
  queryFn: async () => (await api.get(`/tags/${tagId}`)).data,
})

watch(
  tag,
  (t) => {
    if (!t) return
    data.id = t.id
    data.text = t.text
    data.color = t.color
  },
  { immediate: true },
)

const goToList = () => {
  router.push({ name: 'tags' })
}
</script>

<template>
  <ProgressSpinner v-if="isPending" />
  <div v-else-if="isError" class="load-error">Не удалось загрузить тег</div>

  <MyForm
    v-else
    title="Обновить тег"
    :data="data"
    url="tags/update"
    :success_function="goToList"
    :mutated_keys_list="['tags']"
    success_message="Тег обновлён"
  >
    <MyTextInput v-model="data.text" label="Название" />
    <MyColorPicker v-model="data.color" label="Цвет" />

    <template #other_buttons>
      <TagUntieButton :tag-id="data.id" :tag-text="data.text" />
      <DeleteConfirmButton query-key="tags" :object_id="data.id" @deleted="goToList" />
    </template>
  </MyForm>
</template>
