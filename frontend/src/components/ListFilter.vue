<script lang="ts" setup>
import { ref, watch, onBeforeUnmount } from 'vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue'
import MySelect from '@/components/inputs/MySelect.vue'
import MyButton from '@/components/MyButton.vue'

// Универсальная панель фильтра для списков (записи/задачи).
// Работает с реактивным объектом фильтра из стора: мутирует его напрямую,
// поэтому состояние живёт в сторе и не обнуляется между переходами.
interface Filter {
  search: string
  tag_ids: number[]
}

const props = defineProps<{
  filter: Filter
  searchPlaceholder?: string
}>()

const emit = defineEmits<{ reset: [] }>()

const tagsApiUrl = 'tags/'

// Локальное поле поиска с дебаунсом — чтобы не слать запрос на каждый символ.
const searchInput = ref(props.filter.search)
let debounceId: ReturnType<typeof setTimeout> | undefined

watch(searchInput, (value) => {
  if (debounceId) clearTimeout(debounceId)
  debounceId = setTimeout(() => {
    props.filter.search = value
  }, 400)
})

// Если фильтр сбросили извне — синхронизируем локальное поле.
watch(
  () => props.filter.search,
  (value) => {
    if (value !== searchInput.value) searchInput.value = value
  },
)

onBeforeUnmount(() => {
  if (debounceId) clearTimeout(debounceId)
})

const updateTags = (value: unknown) => {
  props.filter.tag_ids = Array.isArray(value) ? (value as number[]) : []
}

const reset = () => {
  searchInput.value = ''
  emit('reset')
}
</script>

<template>
  <div class="list-filter">
    <MyTextInput
      v-model="searchInput"
      label="Поиск"
      :placeholder="searchPlaceholder ?? 'Найти по тексту...'"
    />

    <MySelect
      option-label="text"
      option-value="id"
      :model-value="filter.tag_ids"
      multiple
      :api-url="tagsApiUrl"
      label="Теги"
      placeholder="Любые теги"
      @update:model-value="updateTags"
    />

    <MyButton size="small" severity="secondary" class="list-filter__reset" @click="reset">
      Сбросить фильтр
    </MyButton>
  </div>
</template>

<style scoped>
.list-filter {
  display: flex;
  flex-direction: column;
}

.list-filter__reset {
  align-self: flex-start;
}
</style>
