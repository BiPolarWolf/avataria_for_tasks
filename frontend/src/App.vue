
<script setup lang="ts">
import GameContainer from '@/GameContainer.vue'
import {ScrollPanel} from 'primevue';

import { Toast } from 'primevue';

</script>

<template>
  <Toast></Toast>
  <div class="h-screen mx-auto flex flex-row">

      <div class="basis-6/12 bg-paper">

       <nav class="p-4 bg-paper-orange h-1/12">
          <RouterLink class="p-2 bg-gray-500" to="/"> Главная </RouterLink>
          <RouterLink class="p-2 bg-gray-500 " to="/about"> О проекте </RouterLink>
          <RouterLink class="p-2 bg-gray-500" to="/profile"> О нас </RouterLink> 
          <RouterLink class="p-2 bg-gray-500" to="/tasks"> Задачи </RouterLink> 
          <RouterLink class="p-2 bg-gray-500 " to="/login"> Войти </RouterLink>
        </nav>

        <div class="m-auto h-11/12 bg-paper">
        <ScrollPanel class="custom_scroll_panel" style="width: 98%; height: 100%; padding: 10px;"  >
          <RouterView />
        </ScrollPanel>
        </div>


      </div>
      <div class="basis-6/12 bg-paper-orange window">
        <GameContainer/>
      </div>
  </div>


</template>

<style scoped>

.custom_scroll_panel :deep(.p-scrollpanel-bar-y){
    background-color: rgb(115 85 63);
}

.window{
  border: 15px solid rgb(115 85 63);
}

</style>

