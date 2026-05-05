
<script setup lang="ts">
import GameContainer from '@/GameContainer.vue'
import {SplitterPanel, Splitter} from 'primevue';

import { Toast } from 'primevue';

</script>

<template>
  <Toast></Toast>
  <div class="h-screen mx-auto flex flex-row">

      <div class="basis-6/12 bg-paper">

       <nav class="p-4 bg-paper-orange">
          <RouterLink class="p-2 bg-gray-500" to="/"> Главная </RouterLink>
          <RouterLink class="p-2 bg-gray-500 " to="/about"> О проекте </RouterLink>
          <RouterLink class="p-2 bg-gray-500" to="/profile"> О нас </RouterLink> 
          <RouterLink class="p-2 bg-gray-500" to="/tasks"> Задачи </RouterLink> 
          <RouterLink class="p-2 bg-gray-500 " to="/login"> Войти </RouterLink>
        </nav>

        <div class="p-4 m-auto h-max bg-paper mt-2">
          <RouterView class="h-max" />
        </div>

      </div>
      <div class="basis-6/12 bg-paper-orange">
        <GameContainer/>
      </div>
  </div>



</template>

