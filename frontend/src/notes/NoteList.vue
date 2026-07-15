<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import { formatShortDate } from '@/utils/general'
import { ref, type Ref } from 'vue'
import Tag from '@/tags/Tag.vue'
import ApiContainer from '@/components/ApiContainer.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'
import MyButton from '@/components/MyButton.vue'
import NoteUpdateDialog from './NoteUpdateDialog.vue'
import { useSettingsStore } from '@/stores/settings'


const settingsStore = useSettingsStore()

const {showNotesText }  = settingsStore

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
  <NoteUpdateDialog v-model:visible="visible" v-model:initial="selected_note" ></NoteUpdateDialog>

  <ApiContainer apiUrl="/notes/"  :queryKeys="['notes']">
    <template v-slot:default="{ data }">
      <MyCard class="my-3" v-for="note in data">
      <template #content>
        


        <template v-if=" showNotesText || opened_notes.includes(note.id)">
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

          <template v-if=" !showNotesText">
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
          </template>

          <MyButton size="small" severity="info" v-on:click="() =>update_note(note)"  class="detail_button">
              Изменить  <img src="@/assets/icons/Wrench.png" style="width: 18px;" alt="">
          </MyButton>

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
  background-color: var(--muted);
  border: 4px solid var(--text);
  color: var(--accent-text);
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