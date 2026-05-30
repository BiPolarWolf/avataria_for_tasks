
<script setup lang="ts">
import GameContainer from '@/GameContainer.vue'
import {ScrollPanel} from 'primevue';
import { useAuthStore } from './stores/auth';
import { Toast } from 'primevue';
import MyButton from './components/MyButton.vue';

const authStore = useAuthStore()

</script>

<template>
  <Toast></Toast>
  <div class="h-screen mx-auto flex flex-row">

      <div class="basis-6/12">

       <nav class=" h-1/12 content-center justify-content-center justify-center">

      <div class="nav_row">
        <div class="nav_group">
          <RouterLink class="ui-btn" to="/"> Главная </RouterLink>
          <RouterLink class="ui-btn" to="/notes"><i class="pi pi-book"></i> Записи </RouterLink>
          <RouterLink class="ui-btn" to="/tasks"><i class="pi pi-check-square"></i> Задачи </RouterLink> 
          <RouterLink class="ui-btn" to="/tags"><i class="pi pi-tag"></i> Теги </RouterLink>
        </div>

        
          <div class="nav_group nav_group--right">

            <div v-if="!authStore.isAuthenticated" >
            <RouterLink  class="ui-btn" to="/login"> Войти </RouterLink>
            </div>
            
            <div v-else class="nav_group">
            <RouterLink class="ui-btn" to="/profile">
              <img src="@/assets/icons/Briefcase.png" alt="">
              {{ authStore.user?.username }}
            </RouterLink> 
              <button class="ui-btn ui-btn--danger "  v-on:click="()=>authStore.logout()">Выйти</button>
            </div>

          </div>
        </div>
          
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

.nav_row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-right: 0.75rem;
}

.nav_group {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.1rem;
}

.nav_group--right {
  justify-content: flex-end;
}

.nav_link {
  padding: 15px;
  margin: 0px 2px ;
  border : 5px solid var(--color-secondary-900);
  background-color: var(--color-secLinondary-600);
  color: wheat
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
