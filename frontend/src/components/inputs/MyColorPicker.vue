<script lang="ts" setup>
import { computed } from 'vue'
import ColorPicker from 'primevue/colorpicker'

interface Props {
  modelValue: string
  label?: string
  error?: string
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '#EAD7BB',
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const colorWithoutHash = computed(() => props.modelValue.replace('#', '') || 'EAD7BB')
const previewColor = computed(() => `#${colorWithoutHash.value}`)

const updateColor = (value: string) => {
  emit('update:modelValue', `#${value.replace('#', '')}`)
}

const updateManualColor = (event: Event) => {
  const value = (event.target as HTMLInputElement).value.trim()
  emit('update:modelValue', value.startsWith('#') ? value : `#${value}`)
}
</script>

<template>
  <div class="field-container">
    <label v-if="label" class="pixel-label">{{ label }}</label>

    <div :class="['color-row', { 'input-error': error }]">
      <div class="picker-shell">
        <ColorPicker
          :model-value="colorWithoutHash"
          format="hex"
          input-id="color-picker"
          @update:model-value="updateColor"
        />
      </div>

      <div class="color-preview" :style="{ backgroundColor: previewColor }" />

      <input
        class="color-input"
        :value="modelValue"
        :placeholder="placeholder"
        maxlength="7"
        @input="updateManualColor"
      >
    </div>

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
  color: var(--color-paper-800);
  padding-left: 5px;
}

.color-row {
  display: grid;
  grid-template-columns: auto 42px minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 10px;
  border: 3px solid var(--color-paper-500);
  border-radius: 0;
  background-color: var(--color-paper-50);
  box-shadow: inset 2px 2px 0 var(--color-paper-200);
}

.color-row:focus-within {
  border-color: var(--color-paper-700);
  background-color: #ffffff;
  box-shadow: inset 2px 2px 0 var(--color-paper-300);
}

.picker-shell {
  display: inline-flex;
  padding: 3px;
  border: 2px solid var(--color-paper-700);
  background: linear-gradient(180deg, var(--color-paper-200), var(--color-paper-300));
  box-shadow: 2px 2px 0 rgba(15, 43, 64, 0.22);
}

.color-preview {
  width: 42px;
  height: 42px;
  border: 3px solid var(--color-paper-800);
  box-shadow:
    inset 2px 2px 0 rgba(255, 255, 255, 0.35),
    2px 2px 0 rgba(15, 43, 64, 0.24);
}

.color-input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--color-paper-950);
  font-family: 'PixeloidSans', sans-serif;
  font-size: 0.95rem;
}

.color-input::placeholder {
  color: var(--color-secondary-500);
}

.input-error {
  border-color: var(--color-red-800);
  background-color: var(--color-red-100);
}

.error-text {
  color: var(--color-red-800);
  font-size: 0.8rem;
  font-weight: bold;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.p-colorpicker-preview) {
  width: 34px !important;
  height: 34px !important;
  border: 0 !important;
  border-radius: 0 !important;
  cursor: pointer;
}
</style>

<style>
.p-colorpicker-panel {
  border: 3px solid var(--color-paper-700) !important;
  border-radius: 0 !important;
  background: var(--color-paper-50) !important;
  box-shadow:
    inset 2px 2px 0 var(--color-paper-200),
    5px 5px 0 rgba(15, 43, 64, 0.35) !important;
}
</style>
