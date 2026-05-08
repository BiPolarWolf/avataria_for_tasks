<script lang='ts' setup>
import { ref } from 'vue';

interface Props {
  modelValue: number;
  label?: string;
  max?: number;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: 1,
  label: 'Сложность квеста',
  max: 5
});

const emit = defineEmits(['update:modelValue']);

// Состояние для предпросмотра при наведении
const hoverValue = ref(0);

const setRating = (val: number) => {
  emit('update:modelValue', val);
};


</script>

<template>
  <div class="field-container font-pixel">
    <label v-if="label" class="pixel-label">{{ label }}</label>
    
    <div class="stars-wrapper" @mouseleave="hoverValue = 0">
      <div 
        v-for="i in max" 
        :key="i"
        class="star-item"
        @mouseenter="hoverValue = i"
        @click="setRating(i)"
      >

        <img class="pixel-star" 
        :class="{ 'is-active': i <= (hoverValue || modelValue) }"
        src="@/assets/icons/CatHead.png" alt="test">

      </div>
    </div>
  </div>
</template>

<style scoped>
.field-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.pixel-label {
  font-weight: bold;
  font-size: 0.85rem;
  color: var(--color-paper-800);
}

.stars-wrapper {
  display: flex;
  gap: 4px;
}

.star-item {
  cursor: pointer;
  width: 32px;
  height: 32px;
  transition: transform 0.1s;
}

.star-item:hover {
  transform: scale(1.1);
}

.star-item:active {
  transform: scale(0.9);
}

.pixel-star {
  width: 100%;
  height: 100%;
  
  /* Состояние "не активен": блеклый и серый */
  opacity: 0.3;
  filter: grayscale(100%);
  
  /* Сохраняем четкость пикселей для вашего RPG стиля */
  image-rendering: pixelated; 
  transition: all 0.2s ease;
}

/* Состояние "активен": цветной и яркий */
.pixel-star.is-active {
  opacity: 1;
  filter: grayscale(0%) drop-shadow(0 0 2px rgba(255, 215, 0, 0.5));
}

.pixel-star.is-active .star-fill {
  fill: #ffd700; /* Золотой пиксель */
}

/* Если звезда не активна, заливка сливается с фоном или бумагой */
.pixel-star:not(.is-active) .star-fill {
  fill: var(--color-paper-50);
}

/* Плавная смена цвета */
.star-fill {
  transition: fill 0.1s;
}
</style>