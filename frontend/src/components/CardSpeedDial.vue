<script setup lang="ts">
import SpeedDial from 'primevue/speeddial'

export interface CardSpeedDialItem {
  label: string
  icon: string
  command: () => void
  severity?: 'info' | 'success' | 'danger' | 'secondary' | 'primary'
  disabled?: boolean
}

interface Props {
  items: CardSpeedDialItem[]
  direction?: 'up' | 'down' | 'left' | 'right'
  ariaLabel?: string
}

withDefaults(defineProps<Props>(), {
  direction: 'left',
  ariaLabel: 'Действия',
})
</script>

<template>
  <SpeedDial
    :model="items"
    :direction="direction"
    type="linear"
    :transition-delay="60"
    show-icon="pi pi-ellipsis-v"
    hide-icon="pi pi-times"
    :rotate-animation="false"
    hide-on-click-outside
    button-class="ui-btn ui-btn--icon ui-btn--secondary"
    :aria-label="ariaLabel"
    class="card-speeddial"
  >
    <template #item="{ item, onClick }">
      <button
        type="button"
        class="ui-btn ui-btn--icon"
        :class="item.severity ? `ui-btn--${item.severity}` : 'ui-btn--secondary'"
        :disabled="!!item.disabled"
        :title="String(item.label ?? '')"
        :aria-label="String(item.label ?? '')"
        @click="onClick"
      >
        <i :class="item.icon"></i>
      </button>
    </template>
  </SpeedDial>
</template>

<style scoped>
.card-speeddial {
  align-items: center;
}
</style>
