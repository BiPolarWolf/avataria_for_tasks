<script setup lang="ts">
// Правая панель раздела «Теги»: действия над списком.
// Создание вынесено на маршрут /tags/create (форма открывается в центре).
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">Действия</p>
    <RouterLink class="ui-btn ui-btn--primary aside__cta" :to="{ name: 'tags-create' }">
      <i class="pi pi-plus"></i>&nbsp;Создать тег
    </RouterLink>
  </div>
</template>
