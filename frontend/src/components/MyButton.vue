<script setup lang="ts">
import Button from 'primevue/button'

defineOptions({
  inheritAttrs: false,
})
</script>

<template>
  <Button v-bind="$attrs" class="ui-btn mx-0.5 ">
    <slot></slot>
  </Button>
</template>
