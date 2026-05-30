<script lang='ts' setup>
import { ref, computed } from 'vue'


interface Tag {
  id: number
  text: string
  color: string
  icon: string
}

interface Props {
  tag: Tag
}

const props = defineProps<Props>()


</script>

<template>
    <div :style="{ backgroundColor: tag.color }" class="tag">{{ props.tag.text }}</div>
</template>

<style scoped>
    .tag {
        display: inline-block;
        padding: 3px 6px;
        border-radius: 5px;
        border: 2px solid var(--color-secondary-400);
        font-size: 14px;
        font-weight: 500;
        margin-right: 0.5rem;
    }
</style>

