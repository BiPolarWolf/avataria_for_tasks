<script setup lang="ts">
import ApiContainer from '@/components/ApiContainer.vue';
import Tag from './Tag.vue';
import TagUpdateDialog from './TagUpdateDialog.vue';
import { ref } from 'vue';



const selected_tag = ref(null)
const visible = ref(false)

const update_tag = (tag:any) => {
  selected_tag.value = tag
  visible.value = true
};


</script>

<template>
  <TagUpdateDialog v-model:visible="visible" v-model:initial="selected_tag" />

  <ApiContainer apiUrl="/tags/" :queryKeys="['tags']">
    <template v-slot:default="{ data }">
      <div>
        <span v-for="tag in data" :key="tag.id">
            <Tag :tag="tag" @click="update_tag(tag)" />
        </span>
      </div>
    </template>
  </ApiContainer>
</template>
