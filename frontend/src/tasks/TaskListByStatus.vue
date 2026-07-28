<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import Tag from '@/tags/Tag.vue'
import CardSpeedDial, { type CardSpeedDialItem } from '@/components/CardSpeedDial.vue'
import { formatShortDate } from '@/utils/general'
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import TaskCompleteConfirmButton from './TaskCompleteConfirmButton.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'
import { useFiltersStore, buildFilterQuery } from '@/stores/filters'

import ApiContainer from '@/components/ApiContainer.vue';


interface Props {
  status: "active" | 'completed'
}

const props = defineProps<Props>()

const router = useRouter()
const filtersStore = useFiltersStore()

// Фильтр (поиск + теги) из стора превращаем в query-строку и ключ кэша.
// Запрос уходит в базу; ключ включает статус и фильтр — список обновляется при их смене.
const apiUrl = computed(() => `/tasks/${props.status}${buildFilterQuery(filtersStore.tasks)}`)
const queryKeys = computed(() => [
  'tasks',
  props.status,
  filtersStore.tasks.search.trim(),
  [...filtersStore.tasks.tag_ids],
])

const edit_task = (task_id:number) => {
  router.push({ name: 'tasks-edit', params: { id: task_id } })
};

// Диалоги подтверждения живут в скрытых экземплярах кнопок (hide-trigger) —
// SpeedDial по клику на пункт меню лишь открывает нужный диалог через ref.
const completeRefs: Record<number, InstanceType<typeof TaskCompleteConfirmButton> | null> = {}
const deleteRefs: Record<number, InstanceType<typeof DeleteConfirmButton> | null> = {}

const buildActions = (task: { id: number; description: string }): CardSpeedDialItem[] => [
  {
    label: 'Изменить',
    icon: 'pi pi-pencil',
    severity: 'info',
    command: () => edit_task(task.id),
  },
  {
    label: 'Выполнить',
    icon: 'pi pi-check',
    severity: 'success',
    command: () => completeRefs[task.id]?.open(),
  },
  {
    label: 'Удалить',
    icon: 'pi pi-trash',
    severity: 'danger',
    command: () => deleteRefs[task.id]?.open(),
  },
]
</script>


<template>

    <ApiContainer :api-url="apiUrl"  :queryKeys="queryKeys">
      <template v-slot:default="{ data}">

        <p v-if="!data.length" class="empty-hint">Ничего не найдено. Попробуйте изменить фильтр.</p>

        <MyCard class="my-3" v-for="task in data" :key="task.id">
          <template #content>
          <p class="task_description">{{ task.description }}</p>
          <br>
          <p >Сложность: <img class="w-6 inline" v-for="value in task.complexity"  src="@/assets/icons/CatHead.png" alt="()"></p>

          <p class="mt-3" v-if="task.tags && task.tags.length">
            Теги:
            <template v-for="tag in task.tags" :key="tag.id">
              <Tag :tag="tag" />
            </template>
          </p>
          </template>

          <template #subtitle>
              <span v-if="task.title" class="font-bold">{{ task.title }}</span>
              {{ formatShortDate(task.created_at) }} {{ task.completed_at ? `- ${formatShortDate(task.completed_at)}` : "" }}
          </template>


          <template #buttons> <span></span></template>

          <template #actions>
            <template v-if="props.status === 'active'">
              <TaskCompleteConfirmButton
                :ref="(el: any) => { completeRefs[task.id] = el }"
                hide-trigger
                :task-id="task.id"
                :task-description="task.description"
              />
              <DeleteConfirmButton
                :ref="(el: any) => { deleteRefs[task.id] = el }"
                hide-trigger
                :object_id="task.id"
                :description="task.description"
                :query-key="'tasks'"
              />
              <CardSpeedDial :items="buildActions(task)" />
            </template>
            <template v-else>
              <span>Завершено</span>
            </template>
          </template>

      </MyCard>


      </template>
    </ApiContainer>



</template>

<style scoped>

.task_description {
  white-space: pre-wrap;
}

.empty-hint {
  padding: 1rem;
  color: var(--muted);
}

.task_error {
  padding: 1rem;
  border: 3px solid var(--border-strong);
  background: color-mix(in srgb, var(--surface) 92%, transparent);
  color: var(--text);
}

</style>
