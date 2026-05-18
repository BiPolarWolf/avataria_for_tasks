<script setup lang="ts">
import Button from 'primevue/button'

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Button  v-bind="$attrs" class="ui-btn m-1">
    <slot></slot>
  </Button>
</template>
