<script setup lang="ts">
import Dialog from 'primevue/dialog'

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Dialog :draggable="false" v-bind="$attrs"
  :pt="{
      root: { class: 'bg-surface !border-none !shadow-none '},
      header: { class: 'bg-surface-sunken text-text !border-none' },
      footer: { class: 'bg-surface-sunken text-text !border-none' },
      content: { class: 'bg-surface' },

      // Стилизация кнопки закрытия
      pcCloseButton: {
        root: {
          class: '!bg-border  hover:!bg-border-strong !text-accent-text !w-8 !h-8 !border-none !shadow-none !outline-none transition-colors'
        }
      }

    }"
  
  >
    <template v-if="$slots.header" #header>
      <slot name="header" />
    </template>

    <slot />

    <template v-if="$slots.footer" #footer>
      <slot name="footer"/>
    </template>
  </Dialog>
</template>

<style scoped>


</style>
