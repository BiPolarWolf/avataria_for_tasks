import { defineStore } from 'pinia'
import { reactive, watch } from 'vue'

// Состояние фильтров списков (записи и задачи).
// Сохраняется в localStorage, поэтому фильтры не обнуляются между
// переходами по страницам и перезагрузками — как и просили.

interface ListFilter {
  search: string
  tag_ids: number[]
}

const emptyFilter = (): ListFilter => ({ search: '', tag_ids: [] })

const loadFilter = (key: string): ListFilter => {
  try {
    const raw = localStorage.getItem(key)
    if (!raw) return emptyFilter()
    const parsed = JSON.parse(raw)
    return {
      search: typeof parsed.search === 'string' ? parsed.search : '',
      tag_ids: Array.isArray(parsed.tag_ids) ? parsed.tag_ids : [],
    }
  } catch {
    return emptyFilter()
  }
}

export const useFiltersStore = defineStore('filters', () => {
  const notes = reactive<ListFilter>(loadFilter('filters.notes'))
  const tasks = reactive<ListFilter>(loadFilter('filters.tasks'))

  watch(notes, (value) => localStorage.setItem('filters.notes', JSON.stringify(value)), { deep: true })
  watch(tasks, (value) => localStorage.setItem('filters.tasks', JSON.stringify(value)), { deep: true })

  function resetNotes() {
    notes.search = ''
    notes.tag_ids = []
  }

  function resetTasks() {
    tasks.search = ''
    tasks.tag_ids = []
  }

  return { notes, tasks, resetNotes, resetTasks }
})

// Собирает query-строку для запроса из фильтра.
export const buildFilterQuery = (filter: ListFilter): string => {
  const params = new URLSearchParams()

  const search = filter.search.trim()
  if (search) params.append('search', search)

  for (const id of filter.tag_ids) {
    params.append('tag_ids', String(id))
  }

  const query = params.toString()
  return query ? `?${query}` : ''
}
