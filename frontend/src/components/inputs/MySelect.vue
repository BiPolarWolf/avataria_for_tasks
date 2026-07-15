<script lang="ts" setup>
import { computed, ref, watch } from 'vue'
import MultiSelect from 'primevue/multiselect'
import Select from 'primevue/select'
import api from '@/client'

type ModelValue = unknown | unknown[] | null
type SelectOption = Record<string, unknown>

interface Props {
  modelValue: ModelValue
  label?: string
  placeholder?: string
  error?: string
  options?: SelectOption[]
  apiUrl?: string
  optionLabel?: string
  optionValue?: string
  multiple?: boolean
  searchPlaceholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Выбери из вариантов',
  searchPlaceholder: 'Найти по названию...',
  optionLabel: 'label',
  optionValue: 'value',
  multiple: false,
  options: () => [],
})

const emit = defineEmits<{
  'update:modelValue': [value: ModelValue]
}>()

const localOptions = ref<SelectOption[]>([])
const isLoading = ref(false)
const loadError = ref<string | null>(null)

const isOnlineMode = computed(() => Boolean(props.apiUrl))
const visibleError = computed(() => props.error || loadError.value)

const updateValue = (value: ModelValue) => {
  emit('update:modelValue', value)
}

const extractOptions = (data: unknown): SelectOption[] => {
  if (Array.isArray(data)) {
    return data as SelectOption[]
  }

  if (
    data &&
    typeof data === 'object' &&
    'items' in data &&
    Array.isArray((data as { items?: unknown }).items)
  ) {
    return (data as { items: SelectOption[] }).items
  }

  return []
}

let requestNumber = 0

const loadOptions = async () => {
  const currentRequest = ++requestNumber
  loadError.value = null

  if (!isOnlineMode.value) {
    localOptions.value = props.options
    return
  }

  isLoading.value = true

  try {
    const data = (await api.get(props.apiUrl as string)).data

    if (currentRequest === requestNumber) {
      localOptions.value = extractOptions(data)
    }
  } catch {
    if (currentRequest === requestNumber) {
      localOptions.value = []
      loadError.value = 'Не удалось загрузить варианты'
    }
  } finally {
    if (currentRequest === requestNumber) {
      isLoading.value = false
    }
  }
}

watch(
  () => [props.options, props.apiUrl] as const,
  loadOptions,
  { immediate: true },
)
</script>

<template>
  <div class="field-container">
    <label v-if="label" class="pixel-label">{{ label }}</label>

    <div class="input-wrapper">
      <MultiSelect
        v-if="multiple"
        :option-label="optionLabel"
        :option-value="optionValue"
        :options="localOptions"
        :model-value="Array.isArray(modelValue) ? modelValue : []"
        :placeholder="placeholder"
        :filter="true"
        :filter-by="optionLabel"
        :filter-placeholder="searchPlaceholder"
        :loading="isLoading"
        display="chip"
        :class="['custom-pixel-select', { 'input-error': visibleError }]"
        panel-class="custom-pixel-select-panel"
        @update:model-value="updateValue"
      />

      <Select
        v-else
        :option-label="optionLabel"
        :option-value="optionValue"
        :options="localOptions"
        :model-value="modelValue"
        :placeholder="placeholder"
        :filter="true"
        :filter-by="optionLabel"
        :filter-placeholder="searchPlaceholder"
        :loading="isLoading"
        :class="['custom-pixel-select', { 'input-error': visibleError }]"
        panel-class="custom-pixel-select-panel"
        @update:model-value="updateValue"
      />
    </div>

    <transition name="fade">
      <span v-if="visibleError" class="error-text">{{ visibleError }}</span>
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

.input-wrapper {
  width: 100%;
}

.custom-pixel-select {
  width: 100%;
  border: 3px solid var(--border) !important;
  border-radius: 0 !important;
  background-color: var(--surface) !important;
  color: var(--text) !important;
  box-shadow: inset 2px 2px 0 var(--surface-sunken);
  font-family: var(--font-body);
}

.custom-pixel-select:hover {
  border-color: var(--border-strong) !important;
}

.custom-pixel-select.p-focus,
.custom-pixel-select:focus-within {
  outline: none !important;
  border-color: var(--border-strong) !important;
  background-color: var(--surface) !important;
  box-shadow: inset 2px 2px 0 var(--accent-subtle);
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.p-select-label),
:deep(.p-multiselect-label) {
  padding: 10px 14px !important;
  color: var(--text) !important;
  font-family: var(--font-body);
}

:deep(.p-select-dropdown),
:deep(.p-multiselect-dropdown) {
  color: var(--muted) !important;
}

:deep(.p-multiselect-label-container) {
  display: flex;
  align-items: center;
  min-width: 0;
}

:deep(.p-multiselect-label) {
  display: flex !important;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  min-height: 45px;
  overflow: visible !important;
  white-space: normal !important;
}

:deep(.p-multiselect-chip) {
  border: 2px solid var(--border-strong);
  border-radius: 0;
  background: linear-gradient(180deg, var(--surface-sunken), var(--accent-subtle));
  color: var(--text);
  font-size: 0.78rem;
  box-shadow: 2px 2px 0 var(--shadow);
}

:deep(.p-placeholder) {
  color: var(--muted) !important;
}
</style>

<style>
.custom-pixel-select-panel {
  border: 3px solid var(--border-strong) !important;
  border-radius: 0 !important;
  background: var(--surface) !important;
  box-shadow:
    inset 2px 2px 0 var(--surface-sunken),
    5px 5px 0 var(--shadow) !important;
  color: var(--text) !important;
  font-family: var(--font-body);
}

.custom-pixel-select-panel .p-select-list,
.custom-pixel-select-panel .p-multiselect-list {
  padding: 6px !important;
  background: var(--surface) !important;
}

.custom-pixel-select-panel .p-select-option,
.custom-pixel-select-panel .p-multiselect-option {
  margin-bottom: 4px;
  border-radius: 0 !important;
  color: var(--text) !important;
}

.custom-pixel-select-panel .p-select-option:hover,
.custom-pixel-select-panel .p-multiselect-option:hover,
.custom-pixel-select-panel .p-select-option.p-focus,
.custom-pixel-select-panel .p-multiselect-option.p-focus {
  background: var(--surface-sunken) !important;
}

.custom-pixel-select-panel .p-select-option.p-select-option-selected,
.custom-pixel-select-panel .p-multiselect-option.p-multiselect-option-selected {
  background: var(--accent-subtle) !important;
  color: var(--text) !important;
  font-weight: 700;
}

.custom-pixel-select-panel .p-select-header,
.custom-pixel-select-panel .p-multiselect-header {
  border-bottom: 3px solid var(--accent-subtle) !important;
  border-radius: 0 !important;
  background: var(--surface-raised) !important;
}

.custom-pixel-select-panel .p-select-filter,
.custom-pixel-select-panel .p-multiselect-filter {
  border: 3px solid var(--border) !important;
  border-radius: 0 !important;
  background: var(--surface) !important;
  color: var(--text) !important;
  font-family: var(--font-body);
}

.custom-pixel-select-panel .p-checkbox-box {
  border: 2px solid var(--border-strong) !important;
  border-radius: 0 !important;
}

.custom-pixel-select-panel .p-checkbox-checked .p-checkbox-box {
  border-color: var(--accent) !important;
  background: var(--accent) !important;
}
</style>
