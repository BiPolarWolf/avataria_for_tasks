<script setup lang='ts'>
import { computed } from 'vue';
import TagUpdateDialog from './TagUpdateDialog.vue';

interface Tag {
id: number
text: string
color: string
icon: string
}

interface Props {
tag: Tag
}

const props = defineProps<Props>()

const tagStyles = computed(() => {
  const bgColor = props.tag.color;
  if (!bgColor) return {};

  // Очищаем цвет от решетки и разворачиваем короткий hex (#fff -> #ffffff)
  let hex = bgColor.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c + c).join('');
  
  // Переводим в RGB
  const r = parseInt(hex.slice(0, 2), 16);
  const g = parseInt(hex.slice(2, 4), 16);
  const b = parseInt(hex.slice(4, 6), 16);
  
  // Формула YIQ для определения воспринимаемой яркости
  const yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
  const isLight = yiq >= 128;

  return {
    backgroundColor: bgColor,
    // Темный текст для светлого фона и белый — для темного
    color: isLight ? '#1f2937' : '#ffffff',
    // Полупрозрачная рамка адаптируется под фон, делая его контур выразительнее
    borderColor: isLight ? 'rgba(0, 0, 0, 0.2)' : 'rgba(255, 255, 255, 0.3)'
  };
});
</script>

<template>
    <div :style="tagStyles" class="tag">{{ props.tag.text }}</div>
</template>

<style scoped>
.tag {
    display: inline-block;
    padding: 3px 6px;
    border-radius: 5px;
    border: 2px solid; /* Цвет задается через inline-стили */
    font-size: 14px;
    font-weight: 500;
    margin-right: 0.5rem;
}
</style>