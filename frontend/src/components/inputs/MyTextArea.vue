<script lang='ts' setup>
import Textarea from 'primevue/textarea';
import { watch } from 'vue';

interface Props {
  modelValue: string;
  label?: string;
  placeholder?: string;
  error?: string;
  rows?: number;
  autoResize?: boolean;
  is_restricted?: boolean;
  symbol_restriction?: number;
}

// Устанавливаем дефолтные значения для рядов
const props = withDefaults(defineProps<Props>(), {
  rows: 3,
  autoResize: true,
  is_restricted: false,
  symbol_restriction: 1000,
});

// Убедись, что emit предварительно объявлен (если это <script setup>)
// const emit = defineEmits(['update:modelValue']);

const emit = defineEmits(['update:modelValue']);

watch(
  () => props.modelValue, 
  (value) => {
    // Добавлена проверка на наличие value, чтобы не получить ошибку, если придет null или undefined
    if (props.is_restricted && value && value.length > props.symbol_restriction) {
      emit('update:modelValue', value.slice(0, props.symbol_restriction));
    }
  }
)


</script>

<template>
  <div class="field-container font-pixel">

    <!-- Label -->
    <label v-if="label" class="pixel-label">
    {{ label }}
      <span v-if="is_restricted">
        {{ modelValue.length }} / {{ symbol_restriction }} 
      </span>
    </label>

    <div class="input-wrapper">
      <Textarea
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
        :placeholder="placeholder"
        :rows="rows"
        :auto-resize="autoResize"
        :class="['custom-pixel-input', { 'input-error': error }]"
      />
    </div>

    <!-- Error message -->
    <transition name="fade">
      <span v-if="error" class="error-text">{{ error }}</span>
    </transition>
  </div>
</template>

<style scoped>
/* Копируем стили из InputText для консистентности */
.field-container {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  width: 100%;
}

.pixel-label {
  font-weight: bold;
  font-size: 0.85rem;
  color: var(--color-paper-800);
  padding-left: 5px;
}

.custom-pixel-input {
  background-color: var(--color-paper-50) !important;
  color: var(--color-paper-950) !important;
  border: 3px solid var(--color-paper-500) !important;
  border-radius: 0 !important;
  padding: 10px 14px;
  width: 100%;
  box-shadow: inset 2px 2px 0px var(--color-paper-200);
  font-family: inherit; /* Чтобы наследовался пиксельный шрифт */
  resize: none; /* Отключаем стандартный ресайз, если используем autoResize */
}

.custom-pixel-input:focus {
  outline: none !important;
  border-color: var(--color-paper-700) !important;
  background-color: #ffffff !important;
  box-shadow: inset 2px 2px 0px var(--color-paper-300);
}

.input-error {
  border-color: var(--color-red-800) !important;
  background-color: var(--color-red-100) !important;
}

.error-text {
  color: var(--color-red-800);
  font-size: 0.8rem;
  font-weight: bold;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>