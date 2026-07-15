<script setup lang="ts">
import MyCard from '@/components/MyCard.vue'
import MyButton from '@/components/MyButton.vue'
import { formatShortDate } from '@/utils/general'
import { ref } from 'vue'
import TaskUpdateDialog from './TaskUpdateDialog.vue'
import TaskCompleteConfirmButton from './TaskCompleteConfirmButton.vue'
import DeleteConfirmButton from '@/components/DeleteConfirmButton.vue'

import ApiContainer from '@/components/ApiContainer.vue';


interface Props {
  status: "active" | 'completed'
}

const props = defineProps<Props>()


const selected_task = ref(null)
const visible = ref(false)

const update_task = (task:any) => {
  visible.value = true
  selected_task.value = task
};
</script>


<template>
  
    <TaskUpdateDialog v-model:visible="visible" v-model:initial="selected_task" />

    <ApiContainer :api-url="`/tasks/${props.status}`"  :queryKeys="['tasks', props.status]">
      <template v-slot:default="{ data}">
        
        <MyCard class="my-3" v-for="task in data">
          <template #content>
          <p class="task_description">{{ task.description }}</p>
          <br>
          <p >Сложность: <img class="w-6 inline" v-for="value in task.complexity"  src="@/assets/icons/CatHead.png" alt="()"></p>
          </template>

          <template #subtitle> 
              {{ formatShortDate(task.created_at) }} {{ task.completed_at ? `- ${formatShortDate(task.completed_at)}` : "" }}
          </template>


          <template #buttons> <span></span></template>

          <template #actions>
            <template v-if="props.status === 'active'">

              <MyButton
              size="small" severity="info" v-on:click="() =>update_task(task)"  class="detail_button">
                  Изменить  <img src="@/assets/icons/Wrench.png" style="width: 18px;" alt="">
              </MyButton>

              <TaskCompleteConfirmButton
                :task-id="task.id"
                :task-description="task.description"
              />
              <DeleteConfirmButton
                :object_id="task.id"
                :description="task.description"
                :query-key="'tasks'"
              />
            </template>
            <template v-else>
              <span>Завершено</span>
            </template>
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


.task_description {
  white-space: pre-wrap;
}

.task_error {
  padding: 1rem;
  border: 3px solid var(--border-strong);
  background: color-mix(in srgb, var(--surface) 92%, transparent);
  color: var(--text);
}

</style>
