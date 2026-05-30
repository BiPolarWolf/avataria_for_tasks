<script lang='ts' setup>
import api from '@/client';
import { useQuery } from '@tanstack/vue-query';
import { ProgressSpinner } from 'primevue';

interface Props {
    apiUrl: string
    queryKeys: string[]
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

// Основной хук Vue Query
const {isPending, isFetching, isError, data, error } = useQuery({
  queryKey: props.queryKeys, // Разделяем кэш по статусу задач
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
  border: 3px solid var(--color-secondary-700);
  background: rgba(241, 226, 204, 0.92);
  color: var(--color-secondary-900);
}

</style>

