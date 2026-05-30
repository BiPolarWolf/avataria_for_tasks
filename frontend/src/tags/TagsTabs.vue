<script setup lang="ts">
import MyTabs from '@/components/MyTabs.vue'
import TagsList from './TagsList.vue';
import TagCreate from './TagCreate.vue';

const tabs = [
  {value : 'create_form', title : 'Создать тег'},
  {value : 'active', title : 'Активные теги'},

]
</script>

<template>
    <MyTabs :tabs="tabs" default_value="active">

      <template #create_form>
        <TagCreate />
      </template>

      <template #active>
        <TagsList></TagsList>
      </template>


      
    </MyTabs>
</template>
