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
  color: var(--muted);
  padding-left: 5px;
}

.color-row {
  display: grid;
  grid-template-columns: auto 42px minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 8px 10px;
  border: 3px solid var(--border);
  border-radius: 0;
  background-color: var(--surface);
  box-shadow: inset 2px 2px 0 var(--surface-sunken);
}

.color-row:focus-within {
  border-color: var(--border-strong);
  background-color: var(--surface);
  box-shadow: inset 2px 2px 0 var(--accent-subtle);
}

.picker-shell {
  display: inline-flex;
  padding: 3px;
  border: 2px solid var(--border-strong);
  background: linear-gradient(180deg, var(--surface-sunken), var(--accent-subtle));
  box-shadow: 2px 2px 0 var(--shadow);
}

.color-preview {
  width: 42px;
  height: 42px;
  border: 3px solid var(--border-strong);
  box-shadow:
    inset 2px 2px 0 rgba(255, 255, 255, 0.35),
    2px 2px 0 var(--shadow);
}

.color-input {
  width: 100%;
  min-width: 0;
  border: 0;
  outline: 0;
  background: transparent;
  color: var(--text);
  font-family: var(--font-body);
  font-size: 0.95rem;
}

.color-input::placeholder {
  color: var(--muted);
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
  border: 3px solid var(--border-strong) !important;
  border-radius: 0 !important;
  background: var(--surface) !important;
  box-shadow:
    inset 2px 2px 0 var(--surface-sunken),
    5px 5px 0 var(--shadow) !important;
}
</style>
