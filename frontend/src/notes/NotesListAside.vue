<script setup lang="ts">
// Правая панель раздела «Записи»: действия над списком + фильтр.
// Создание вынесено на отдельный маршрут /notes/create (форма открывается в центре).
import ListFilter from '@/components/ListFilter.vue'
import { useFiltersStore } from '@/stores/filters'

const filtersStore = useFiltersStore()
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">Действия</p>
    <RouterLink class="ui-btn ui-btn--primary aside__cta" :to="{ name: 'notes-create' }">
      <i class="pi pi-plus"></i>&nbsp;Создать запись
    </RouterLink>

    <p class="aside__eyebrow">Фильтр</p>
    <ListFilter
      :filter="filtersStore.notes"
      search-placeholder="Найти по заголовку и тексту..."
      @reset="filtersStore.resetNotes"
    />
  </div>
</template>
