<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import PetWidget from '@/components/PetWidget.vue'

const authStore = useAuthStore()

// Клик по любому пункту навигации — чтобы родитель мог закрыть мобильную шторку.
const emit = defineEmits<{ navigate: [] }>()

const nav = [
  { to: '/', label: 'Главная', icon: 'pi-home', exact: true },
  { to: '/notes', label: 'Записи', icon: 'pi-book' },
  { to: '/tasks', label: 'Задачи', icon: 'pi-check-square' },
  { to: '/tags', label: 'Теги', icon: 'pi-tag' },
  { to: '/settings', label: 'Настройки', icon: 'pi-cog' },
]
</script>

<template>
  <aside class="sidebar">
    <!-- Виджет питомца (геймификация) -->
    <PetWidget />

    <nav class="nav" @click="emit('navigate')">
      <RouterLink
        v-for="item in nav"
        :key="item.to"
        class="nav__item"
        :to="item.to"
        :active-class="item.exact ? '' : 'nav__item--active'"
        :exact-active-class="item.exact ? 'nav__item--active' : ''"
      >
        <i class="pi" :class="item.icon"></i>
        <span>{{ item.label }}</span>
      </RouterLink>
    </nav>

    <div class="foot" @click="emit('navigate')">
      <template v-if="authStore.isAuthenticated">
        <RouterLink class="foot__user" to="/profile">
          <span class="foot__avatar">{{ authStore.user?.username?.[0]?.toUpperCase() ?? '?' }}</span>
          <span class="foot__name">{{ authStore.user?.username }}</span>
        </RouterLink>
        <button class="ui-btn ui-btn--danger ui-btn--sm" @click="authStore.logout()">Выйти</button>
      </template>
      <button v-else class="ui-btn ui-btn--danger ui-btn--sm">Войти</button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.9rem 0.75rem;
  background-color: var(--brand-deep);
  color: var(--brand-text);
  overflow-y: auto;
}

/* --- Навигация --- */
.nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.nav__item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.6rem 0.7rem;
  border-radius: 8px;
  color: var(--brand-text);
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.14s;
}
.nav__item .pi { font-size: 1rem; width: 1.15rem; text-align: center; }
.nav__item:hover { background-color: color-mix(in srgb, var(--brand-text) 12%, transparent); }
.nav__item--active { background-color: var(--brand-scrollbar); }
.nav__item:focus-visible { outline: 2px solid var(--brand-text); outline-offset: 1px; }

/* --- Низ: профиль/выход --- */
.foot {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.foot__user {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--brand-text);
  text-decoration: none;
  font-size: 0.85rem;
}
.foot__avatar {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.8rem;
  background: color-mix(in srgb, var(--brand-text) 25%, var(--accent));
}
.foot__name { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.foot .ui-btn { width: 100%; }
</style>
