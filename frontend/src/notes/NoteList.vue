<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { ref, type Ref } from 'vue'
import Tag from '@/tags/Tag.vue'
import ApiContainer from '@/components/ApiContainer.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'
import MyButton from '@/components/MyButton.vue'

const selected_note = ref(null)
const visible = ref(false)

const update_note = (task:any) => {
  visible.value = true
  selected_note.value = task
};

const opened_notes : Ref<number[]> = ref([])

const push_to_opened = (note_id:number) => {
  opened_notes.value.push(note_id)
} 

const delete_from_opened = (note_id:number) => {
  opened_notes.value = opened_notes.value.filter(id => id !== note_id)
} 

</script>

<template>
  <ApiContainer apiUrl="/notes/"  :queryKeys="['notes']">
    <template v-slot:default="{ data }">
      <MyCard class="my-3" v-for="note in data">
      <template #content>

        <template v-if="opened_notes.includes(note.id)">
        <p class="task_description"> {{note.text}} </p>
        <br>
        <p >Важность:  <img class="w-6 inline" v-for="value in note.importans"  src="@/assets/icons/CatHead.png" alt="()"></p>
        </template>


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

          <template v-if="!opened_notes.includes(note.id)">
            <MyButton 
              size="small"
              @click="() => push_to_opened(note.id)" 
            >подробнее</MyButton>
          </template>
          <template v-else>
            <MyButton 
              size="small"
              @click="() => delete_from_opened(note.id)" 
            >скрыть</MyButton>
          </template>

          <DeleteConfirmButton
            size="small"
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