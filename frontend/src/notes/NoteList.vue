<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { computed, ref, type Ref } from 'vue'
import { useRouter } from 'vue-router'
import Tag from '@/tags/Tag.vue'
import ApiContainer from '@/components/ApiContainer.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'
import CardSpeedDial, { type CardSpeedDialItem } from '@/components/CardSpeedDial.vue'
import { useSettingsStore } from '@/stores/settings'
import { useFiltersStore, buildFilterQuery } from '@/stores/filters'


const settingsStore = useSettingsStore()
const filtersStore = useFiltersStore()
const router = useRouter()

const {showNotesText }  = settingsStore

// Фильтр из стора превращаем в query-строку и ключ кэша.
// Запрос идёт в базу; ключ включает фильтр, поэтому список обновляется при его смене.
const apiUrl = computed(() => `/notes/${buildFilterQuery(filtersStore.notes)}`)
const queryKeys = computed(() => ['notes', filtersStore.notes.search.trim(), [...filtersStore.notes.tag_ids]])

const edit_note = (note_id:number) => {
  router.push({ name: 'notes-edit', params: { id: note_id } })
};

const opened_notes : Ref<number[]> = ref([])

const push_to_opened = (note_id:number) => {
  opened_notes.value.push(note_id)
}

const delete_from_opened = (note_id:number) => {
  opened_notes.value = opened_notes.value.filter(id => id !== note_id)
}

// Диалог удаления живёт в скрытом экземпляре DeleteConfirmButton (hide-trigger) —
// SpeedDial по клику на пункт меню лишь открывает его через ref.
const deleteRefs: Record<number, InstanceType<typeof DeleteConfirmButton> | null> = {}

const buildActions = (note: { id: number; text: string }): CardSpeedDialItem[] => {
  const items: CardSpeedDialItem[] = []

  if (!showNotesText) {
    items.push(
      opened_notes.value.includes(note.id)
        ? { label: 'Скрыть', icon: 'pi pi-eye-slash', severity: 'secondary', command: () => delete_from_opened(note.id) }
        : { label: 'Подробнее', icon: 'pi pi-eye', severity: 'secondary', command: () => push_to_opened(note.id) }
    )
  }

  items.push(
    { label: 'Изменить', icon: 'pi pi-pencil', severity: 'info', command: () => edit_note(note.id) },
    { label: 'Удалить', icon: 'pi pi-trash', severity: 'danger', command: () => deleteRefs[note.id]?.open() },
  )

  return items
}

</script>

<template>
  <ApiContainer :apiUrl="apiUrl"  :queryKeys="queryKeys">
    <template v-slot:default="{ data }">
      <p v-if="!data.length" class="empty-hint">Ничего не найдено. Попробуйте изменить фильтр.</p>

      <MyCard class="my-3" v-for="note in data" :key="note.id">
      <template #content>
        


        <template v-if=" showNotesText || opened_notes.includes(note.id)">
        <p class="task_description"> {{note.text}} </p>
        <br>
        <p >Важность:  <img class="w-6 inline" v-for="value in note.importans"  src="@/assets/icons/CatHead.png" alt="()"></p>
        </template>


        <p class="mt-3" v-if="note.tags.length">
          Теги: 
          <template
          v-for="tag in note.tags" 
          :key="tag.id"
          >
          <Tag :tag="tag" />
        </template>
        </p>
        </template>

        <template #subtitle> 
         <span class="font-bold">{{ note.title}}</span> {{ formatShortDate(note.date_update) }}
        </template>

        <template #buttons>
          <span></span>
        </template>

        <template #actions>
          <DeleteConfirmButton
            :ref="(el: any) => { deleteRefs[note.id] = el }"
            hide-trigger
            :object_id="note.id"
            query-key="notes"
            :description="note.text"
          />
          <CardSpeedDial :items="buildActions(note)" />
        </template>

    </MyCard>
    </template>
  </ApiContainer>

</template>

<style scoped>

.task_actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.task_description {
  white-space: pre-wrap;
}

.empty-hint {
  padding: 1rem;
  color: var(--muted);
}

</style>