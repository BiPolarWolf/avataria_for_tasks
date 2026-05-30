<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { ref } from 'vue'
import Tag from '@/components/Tag.vue'
import ApiContainer from '@/components/ApiContainer.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'

const selected_task = ref(null)
const visible = ref(false)

const update_note = (task:any) => {
  visible.value = true
  selected_task.value = task
};

</script>


<template>
  <ApiContainer apiUrl="/notes/"  :queryKeys="['notes']">
    <template v-slot:default="{ data }">
      <MyCard class="my-3" v-for="note in data">

        <template #content>
        <p class="task_description">{{ note.text }}</p>
        <br>
        <p >Важность:  <img class="w-6 inline" v-for="value in note.importans"  src="@/assets/icons/CatHead.png" alt="()"></p>
        <p class="mt-3" v-if="note.tags.length">
          Теги: 
          <template
          v-for="tag in note.tags" 
          :key="tag.id"
          >
          <Tag :tag="tag" />
        </template>
        </p>
        </template>

        <template #subtitle> 
         <span class="font-bold">{{ note.title}}</span> {{ formatShortDate(note.date_update) }}
        </template>
xw

        <template #buttons>
          <span></span>
        </template>

        <template #actions>
          <DeleteConfirmButton
            :object_id="note.id"
            query-key="notes"
            :description="note.text"
          />
        </template>

    </MyCard>
    </template>
  </ApiContainer>

</template>

<style scoped>

.detail_button{
  background-color: var(--color-secondary-500);
  border: 4px solid var(--color-secondary-800);
  color: white;
}

.task_actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.task_description {
  white-space: pre-wrap;
}

</style>