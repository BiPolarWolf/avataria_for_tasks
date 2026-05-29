<script setup lang="ts">
import MyTabs from '@/components/MyTabs.vue'
import NoteCreate from './NoteCreate.vue';
import NoteList from './NoteList.vue';

const tabs = [
  {value : 'create_form', title : 'Создать запись'},
  {value : 'notes', title : 'Мои записи'},


]
</script>

<template>
    <MyTabs :tabs="tabs" default_value="notes">

      <template #create_form>
        <NoteCreate />
      </template>

      <template #notes>
        <NoteList></NoteList>
      </template>

      
    </MyTabs>
</template>


