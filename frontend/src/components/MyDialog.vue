<script setup lang="ts">
import Dialog from 'primevue/dialog'

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Dialog :draggable="false" v-bind="$attrs"
  :pt="{
      root: { class: 'bg-paper-400 !border-none !shadow-none '},
      header: { class: 'bg-paper-500 text-white !border-none' },
      footer: { class: 'bg-paper-500 text-white !border-none' },
      content: { class: 'bg-paper-500' },

      // Стилизация кнопки закрытия
      pcCloseButton: {
        root: { 
          class: '!bg-paper-700  hover:!bg-paper-800 !text-paper-400 !w-8 !h-8 !border-none !shadow-none !outline-none transition-colors' 
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
