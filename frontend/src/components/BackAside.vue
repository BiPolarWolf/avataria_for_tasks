<script setup lang="ts">
import { useRouter } from 'vue-router'

// Универсальная правая панель «Вернуться к списку» — для форм создания и
// редактирования во всех разделах. Текст задаётся через props (в т.ч. из роутера).
const props = defineProps<{
  to: string // имя маршрута списка
  eyebrow: string // подпись сверху
  hint?: string // необязательная подсказка
}>()

const router = useRouter()

function back() {
  router.push({ name: props.to })
}
</script>

<template>
  <div class="aside">
    <p class="aside__eyebrow">{{ eyebrow }}</p>
    <button class="ui-btn aside__cta" @click="back">
      <i class="pi pi-arrow-left"></i>&nbsp;Вернуться к списку
    </button>
    <p v-if="hint" class="aside__hint">{{ hint }}</p>
  </div>
</template>
