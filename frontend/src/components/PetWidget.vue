<script setup lang="ts">
// Виджет питомца (геймификация). Пока статичная заглушка, но данные принимает
// через props — позже подключим реальные (xp, уровень, настроение).
withDefaults(
  defineProps<{
    name?: string
    level?: number
    emoji?: string
  }>(),
  {
    name: 'ФАЗЕР',
    level: 1,
    emoji: '🐣',
  },
)
</script>

<template>
  <div class="pet">
    <div class="pet__screen">{{ emoji }}</div>
    <div class="pet__name">{{ name }}</div>
    <div class="pet__lvl">ур. {{ level }}</div>
  </div>
</template>

<style scoped>
.pet {
  flex-shrink: 0;
  text-align: center;
  padding: 0.75rem 0.5rem;
  border: 2px solid color-mix(in srgb, var(--brand-text) 25%, transparent);
  border-radius: 12px;
  background: color-mix(in srgb, var(--brand-text) 8%, transparent);
  color: var(--brand-text);
}
.pet__screen {
  font-size: 2.4rem;
  line-height: 1;
  padding: 0.6rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  background: color-mix(in srgb, #000 26%, transparent);
  box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--brand-text) 18%, transparent);
}
.pet__name {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
}
.pet__lvl {
  font-size: 0.7rem;
  opacity: 0.75;
  margin-top: 2px;
}
</style>
