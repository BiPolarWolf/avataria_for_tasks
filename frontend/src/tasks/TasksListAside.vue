<script setup lang="ts">
// Правая панель раздела «Задачи»: действия над списком + фильтр.
// Создание вынесено на маршрут /tasks/create (форма открывается в центре).
import ListFilter from '@/components/ListFilter.vue'
import { useFiltersStore } from '@/stores/filters'

const filtersStore = useFiltersStore()
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">Действия</p>
    <RouterLink class="ui-btn ui-btn--success aside__cta" :to="{ name: 'tasks-create' }">
      <i class="pi pi-plus"></i>&nbsp;Создать задачу
    </RouterLink>

    <p class="aside__eyebrow">Фильтр</p>
    <ListFilter
      :filter="filtersStore.tasks"
      search-placeholder="Найти по заголовку и описанию..."
      @reset="filtersStore.resetTasks"
    />
  </div>
</template>
