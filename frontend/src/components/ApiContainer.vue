<script lang='ts' setup>
import api from '@/client';
import { useQuery } from '@tanstack/vue-query';
import { ProgressSpinner } from 'primevue';
import { computed } from 'vue';

interface Props {
    apiUrl: string
    queryKeys: (string | number | number[])[]
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
  return queryError?.response?.data?.detail ?? 'Не удалось загрузить данные'
}


// Функция запроса (теперь она отделена от жизненного цикла компонента)
const fetchFunc = async () => {
  const response = await api.get(props.apiUrl)
  return response.data
}

// Основной хук Vue Query.
// queryKey — computed, чтобы запрос перезапускался при смене фильтров/статуса.
const {isPending, isFetching, isError, data, error } = useQuery({
  queryKey: computed(() => props.queryKeys), // Разделяем кэш по статусу и фильтрам
  queryFn: fetchFunc, // Сама функция запроса
  retry: 1,            // Количество попыток при ошибке
})


</script>

<template>

    <template v-if="isPending">
        <ProgressSpinner />
    </template>
    <div v-else-if="isError" class="error">
        {{ getErrorMessage() }}
    </div>
    <div v-else>
        <slot :data="data"></slot>
    </div>

</template>

<style scoped>

.error {
  padding: 1rem;
  border: 3px solid var(--border-strong);
  background: color-mix(in srgb, var(--surface) 92%, transparent);
  color: var(--text);
}

</style>

