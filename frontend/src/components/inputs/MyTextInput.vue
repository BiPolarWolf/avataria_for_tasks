<script lang='ts' setup>
import InputText from 'primevue/inputtext';

interface Props {
  modelValue: string | number;
  label?: string;
  placeholder?: string;
  error?: string;
}

defineProps<Props>();
defineEmits(['update:modelValue']);
</script>

<template>
  <div class="field-container">
    <!-- Если label передан, показываем его -->
    <label v-if="label" class="pixel-label">{{ label }}</label>
    
    <div class="input-wrapper">
      <InputText
        :value="modelValue"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
        :placeholder="placeholder"
        :class="['custom-pixel-input', { 'input-error': error }]"
      />
    </div>

    <!-- Место для ошибки (понадобится для валидации FastAPI) -->
    <transition name="fade">
      <span v-if="error" class="error-text">{{ error }}</span>
    </transition>
  </div>
</template>

<style scoped>
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
  color: var(--muted);
  padding-left: 5px;
}

.custom-pixel-input {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  border: 3px solid var(--border) !important;
  border-radius: 0 !important;
  padding: 10px 14px;
  width: 100%;
  box-shadow: inset 2px 2px 0px var(--surface-sunken);
}

.custom-pixel-input:focus {
  outline: none !important;
  border-color: var(--border-strong) !important;
  background-color: var(--surface) !important;
  box-shadow: inset 2px 2px 0px var(--accent-subtle);
}

/* Стиль ошибки */
.input-error {
  border-color: var(--color-red-800) !important; /* Темно-красный под стиль бумаги */
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