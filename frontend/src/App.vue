
<script setup lang="ts">
import GameContainer from '@/GameContainer.vue'
import {ScrollPanel} from 'primevue';

import { Toast } from 'primevue';

</script>

<template>
  <Toast></Toast>
  <div class="h-screen mx-auto flex flex-row">

      <div class="basis-6/12">

       <nav class=" h-1/12 content-center justify-content-center justify-center">
          <RouterLink class="nav_link " to="/"> Главная </RouterLink>
          <RouterLink class="nav_link" to="/about"> О проекте </RouterLink>
          <RouterLink class="nav_link" to="/profile"> О нас </RouterLink> 
          <RouterLink class="nav_link" to="/tasks"> Задачи </RouterLink> 
          <RouterLink class="nav_link" to="/login"> Войти </RouterLink>
        </nav>

        <div class="m-auto h-11/12 bg-primary-700">
        <ScrollPanel class="custom_scroll_panel" style="width: 98%; height: 100%; padding: 10px;"  >
          <RouterView />
        </ScrollPanel>
        </div>

      </div>
      <div class="basis-6/12 bg-secondary window">
        <GameContainer/>
      </div>
  </div>


</template>

<style scoped>

nav {
  padding-left: 10px;
  background-color: var(--color-primary-900);
}

.nav_link {
  padding: 15px;
  margin: 0px 2px ;
  border : 5px solid var(--color-secondary-900);
  background-color: var(--color-secondary-600);
  color: wheat
}
.nav_link:hover {
  padding: 16px;
  background-color: var(--color-secondary-500);
}


.custom_scroll_panel :deep(.p-scrollpanel-bar-y){
    background-color: var(--color-primary-600);
}

.window{
  border: 15px solid var(--color-secondary-800);
}
</style>

