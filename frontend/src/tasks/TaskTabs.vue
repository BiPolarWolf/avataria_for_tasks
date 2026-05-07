<script setup lang="ts">
import MyTabs from '@/components/MyTabs.vue'
import TaskListByStatus from './TaskListByStatus.vue';
import TaskCreateForm from './TaskCreateForm.vue';
import TaskUpdateForm from './TaskUpdateForm.vue';

const tabs = [
  {value : 'create_form', title : 'Создать задачу'},
  {value : 'my_create_form', title : 'Создать задачу тест'},
  {value : 'active', title : 'Активные задачи'},
  {value : 'completed', title : 'Завершенные задачи'},

]
</script>

<template>
    <MyTabs :tabs="tabs" default_value="active">


      <template #create_form>
        <TaskCreateForm />
      </template>

      <template #my_create_form>
        <TaskUpdateForm />
      </template>


      <template #active>
        <TaskListByStatus status="active"></TaskListByStatus>
      </template>
      <template #completed>
        <TaskListByStatus status="completed"></TaskListByStatus>
      </template>
    </MyTabs>
</template>


