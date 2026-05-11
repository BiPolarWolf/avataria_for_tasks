<script setup lang="ts">
import Button from 'primevue/button'

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Button v-bind="$attrs" class="my_button m-1">
    <slot></slot>
  </Button>
</template>

<style scoped>
.my_button {
  background: linear-gradient(180deg, var(--color-paper-300) 0%, var(--color-paper-500) 100%) !important;
  border: 3px solid var(--color-paper-800) !important;
  border-radius: 0 !important;
  box-shadow:
    inset 0 2px 0 rgba(255, 255, 255, 0.28),
    4px 4px 0 rgba(15, 43, 64, 0.35) !important;
  color: var(--color-secondary-950) !important;
  font-family: 'PixeloidSans', sans-serif !important;
  font-size: 0.95rem;
  line-height: 1.1;
  font-weight: 500;
  padding: 0.75rem 1rem !important;
  text-transform: none;
  transition:
    transform 0.12s ease,
    box-shadow 0.12s ease,
    background-color 0.12s ease,
    filter 0.12s ease;
}

.my_button:hover:not(.p-disabled) {
  background: linear-gradient(180deg, var(--color-paper-200) 0%, var(--color-paper-400) 100%) !important;
  border-color: var(--color-secondary-800) !important;
  transform: translateY(-1px);
  box-shadow:
    inset 0 2px 0 rgba(255, 255, 255, 0.28),
    5px 5px 0 rgba(15, 43, 64, 0.4) !important;
}

.my_button:active:not(.p-disabled) {
  transform: translate(2px, 2px);
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    2px 2px 0 rgba(15, 43, 64, 0.28) !important;
}

.my_button.p-disabled {
  opacity: 0.65;
  filter: grayscale(0.2);
  cursor: not-allowed;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.2),
    2px 2px 0 rgba(15, 43, 64, 0.2) !important;
}

.my_button.p-button-sm {
  padding: 0.55rem 0.85rem !important;
  font-size: 0.82rem;
}

.my_button.p-button-icon-only {
  width: 2.75rem;
  height: 2.75rem;
  padding: 0 !important;
}

.my_button.p-button-secondary {
  background: linear-gradient(180deg, var(--color-secondary-300) 0%, var(--color-secondary-500) 100%) !important;
  border-color: var(--color-secondary-900) !important;
  color: var(--color-paper-50) !important;
}

.my_button.p-button-secondary:hover:not(.p-disabled) {
  background: linear-gradient(180deg, var(--color-secondary-200) 0%, var(--color-secondary-400) 100%) !important;
}

.my_button.p-button-success {
  background: linear-gradient(180deg, #b9d6a3 0%, #7ea45d 100%) !important;
  border-color: #425f2e !important;
  color: #1f2d14 !important;
}

.my_button.p-button-success:hover:not(.p-disabled) {
  background: linear-gradient(180deg, #c8dfb6 0%, #91b56f 100%) !important;
}

.my_button.p-button-danger {
  background: linear-gradient(180deg, #ef9a86 0%, #c84f3c 100%) !important;
  border-color: #7f2b22 !important;
  color: #fff8f2 !important;
}

.my_button.p-button-danger:hover:not(.p-disabled) {
  background: linear-gradient(180deg, #f3aa98 0%, #d8614d 100%) !important;
}

.my_button.p-button-contrast,
.my_button.p-button-info {
  background: linear-gradient(180deg, var(--color-primary-300) 0%, var(--color-primary-600) 100%) !important;
  border-color: var(--color-primary-900) !important;
  color: var(--color-paper-50) !important;
}

.my_button.p-button-contrast:hover:not(.p-disabled),
.my_button.p-button-info:hover:not(.p-disabled) {
  background: linear-gradient(180deg, var(--color-primary-200) 0%, var(--color-primary-500) 100%) !important;
}

.my_button.p-button-outlined {
  background: rgba(252, 248, 243, 0.72) !important;
  color: var(--color-secondary-900) !important;
}

.my_button.p-button-text {
  background: transparent !important;
  box-shadow: none !important;
  border-color: transparent !important;
}

.my_button :deep(.p-button-label) {
  font-weight: 700;
}

.my_button :deep(.p-button-icon) {
  font-size: 0.95rem;
}
</style>
