<script setup lang="ts">
// Правая панель раздела «Задачи»: действия над списком.
// Создание вынесено на маршрут /tasks/create (форма открывается в центре).
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">Действия</p>
    <RouterLink class="ui-btn ui-btn--success aside__cta" :to="{ name: 'tasks-create' }">
      <i class="pi pi-plus"></i>&nbsp;Создать задачу
    </RouterLink>

    <p class="aside__eyebrow">Фильтр</p>
    <p class="aside__hint">Фильтр по сложности появится здесь.</p>
  </div>
</template>
