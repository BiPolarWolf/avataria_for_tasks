<script setup lang="ts">
// Правая панель раздела «Записи»: действия над списком.
// Создание вынесено на отдельный маршрут /notes/create (форма открывается в центре).
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">Действия</p>
    <RouterLink class="ui-btn ui-btn--primary aside__cta" :to="{ name: 'notes-create' }">
      <i class="pi pi-plus"></i>&nbsp;Создать запись
    </RouterLink>

    <p class="aside__eyebrow">Фильтр</p>
    <p class="aside__hint">Фильтр по тегам и сортировка появятся здесь.</p>
  </div>
</template>
