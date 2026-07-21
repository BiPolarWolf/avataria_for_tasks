<script setup lang="ts">
import { ref } from 'vue'
import TaskListByStatus from './TaskListByStatus.vue'

// Статус — фильтр над списком (бывшие вкладки «Активные / Завершённые»).
const status = ref<'active' | 'completed'>('active')
</script>

<template>
  <div class="tasklist">
    <div class="seg" role="group" aria-label="Статус задач">
      <button
        class="seg__btn"
        :class="{ 'seg__btn--active': status === 'active' }"
        @click="status = 'active'"
      >
        Активные
      </button>
      <button
        class="seg__btn"
        :class="{ 'seg__btn--active': status === 'completed' }"
        @click="status = 'completed'"
      >
        Завершённые
      </button>
    </div>

    <!-- key гарантирует чистый перезапрос при смене статуса -->
    <TaskListByStatus :key="status" :status="status" />
  </div>
</template>

<style scoped>
.tasklist {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.seg {
  display: flex;
  gap: 4px;
  padding: 4px;
  border: 2px solid var(--border);
  border-radius: 10px;
  background: var(--surface-sunken);
}
.seg__btn {
  flex: 1;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  padding: 0.5rem 0.75rem;
  border: 0;
  border-radius: 7px;
  background: transparent;
  color: var(--muted);
  transition: background-color 0.14s, color 0.14s;
}
.seg__btn:hover {
  color: var(--text);
}
.seg__btn--active {
  background: var(--accent);
  color: var(--accent-text);
}
.seg__btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
</style>
