<script setup lang="ts">
import ApiContainer from '@/components/ApiContainer.vue';
import Tag from '@/components/Tag.vue';

</script>

<template>
  <ApiContainer apiUrl="/tags/" :queryKeys="['tags']">
    <template v-slot:default="{ data }">
      <div>
        <h1 class="m-2 text-lg">Теги</h1>
        <br>
        <ul>
        <li v-for="tag in data" :key="tag.id">
            <Tag :tag="tag" />
        </li>
        </ul>
    </div>
    </template>
  </ApiContainer>
</template>

