<script setup lang="ts">
import ApiContainer from '@/components/ApiContainer.vue';
import Tag from './Tag.vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const edit_tag = (tag_id:number) => {
  router.push({ name: 'tags-edit', params: { id: tag_id } })
};
</script>

<template>
  <ApiContainer apiUrl="/tags/" :queryKeys="['tags']">
    <template v-slot:default="{ data }">
      <div>
        <span v-for="tag in data" :key="tag.id">
            <Tag :tag="tag" @click="edit_tag(tag.id)" />
        </span>
      </div>
    </template>
  </ApiContainer>
</template>
