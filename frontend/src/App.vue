
<script setup lang="ts">
import GameContainer from '@/GameContainer.vue'
import { ScrollPanel } from 'primevue'
import { useAuthStore } from './stores/auth'
import { Toast } from 'primevue'
import MyButton from './components/MyButton.vue'

const authStore = useAuthStore()
</script>

<template>
  <Toast />

  <div class="app-shell">
    <header class="topbar">
      <div class="topbar__links">
        <RouterLink class="ui-btn" to="/"> Главная </RouterLink>
        <RouterLink class="ui-btn" to="/notes"><i class="pi pi-book"></i> Записи </RouterLink>
        <RouterLink class="ui-btn" to="/tasks"><i class="pi pi-check-square"></i> Задачи </RouterLink>
        <RouterLink class="ui-btn" to="/tags"><i class="pi pi-tag"></i> Теги </RouterLink>
      </div>

      <div class="topbar__actions">
        <MyButton v-if="!authStore.isAuthenticated" severity="danger">Войти</MyButton>
        <template v-else>
          <RouterLink class="ui-btn" to="/profile">
            {{ authStore.user?.username }}
          </RouterLink>

          <button class="ui-btn ui-btn--danger "  v-on:click="()=>authStore.logout()">Выйти</button>

        </template>

      </div>
    </header>

    <div class="main-layout bg-primary-700">
      <section class="page-panel">
        <ScrollPanel class="page-scroll">
          <div class="page-scroll__content bg-primary-700">
            <RouterView />
          </div>
        </ScrollPanel>
      </section>

      <section class="game-panel">
        <GameContainer />
      </section>
    </div>
  </div>

</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.topbar {
  flex-shrink: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  background-color: var(--color-primary-900);
}

.topbar__links,
.topbar__actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.main-layout {
  flex: 1;
  min-height: 0;
  display: flex;
}

.page-panel {
  flex: 3;
  min-width: 0;
  min-height: 0;
  padding: 0.5rem;
}

.game-panel {
  flex: 2;
  min-width: 0;
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;

}

.page-scroll {
  width: 100%;
  height: 100%;
  min-height: 0;
}

.page-scroll__content {
  min-height: 100%;
  padding: 1rem;
}

.page-scroll :deep(.p-scrollpanel-wrapper) {
  inset: 0;
}

.page-scroll :deep(.p-scrollpanel-content) {
  height: 100%;
}

.page-scroll :deep(.p-scrollpanel-bar-y) {
  background-color: var(--color-primary-600);
}

@media (max-width: 960px) {
  .topbar {
    align-items: stretch;
    flex-direction: column;
  }

  .main-layout {
    display: block;
  }

  .topbar__links,
  .topbar__actions {
    width: 100%;
    flex-direction: column;
    align-items: stretch;
  }

  .topbar__links :deep(.ui-btn),
  .topbar__actions :deep(.ui-btn) {
    width: 100%;
  }

  .page-panel {
    width: 100%;
    flex: none;
  }

  .game-panel {
    display: none;
  }
}
</style>
