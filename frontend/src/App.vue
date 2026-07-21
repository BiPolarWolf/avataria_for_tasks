<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Toast } from 'primevue'
import AppSidebar from '@/components/AppSidebar.vue'

const route = useRoute()

// Правая колонка показывается, только если у текущего роута есть именованный
// компонент right. Отсюда «где-то 2, где-то 3 блока».
const hasRight = computed(() =>
  route.matched.some((r) => r.components && 'right' in r.components),
)

// Заголовок текущего раздела для мобильной шапки.
const title = computed(() => (route.meta.title as string) || 'avataria')

// Мобильные выезжающие панели.
const navOpen = ref(false)
const asideOpen = ref(false)

function closeDrawers() {
  navOpen.value = false
  asideOpen.value = false
}

// При смене роута закрываем шторки.
watch(() => route.fullPath, closeDrawers)
</script>

<template>
  <Toast />

  <div
    class="shell"
    :class="{ 'shell--has-right': hasRight, 'is-nav-open': navOpen, 'is-aside-open': asideOpen }"
  >
    <!-- ЛЕВАЯ: навигация -->
    <div class="shell__sidebar">
      <AppSidebar @navigate="closeDrawers" />
    </div>

    <!-- ЦЕНТР -->
    <main class="shell__center">
      <div class="mobilebar">
        <button class="mobilebar__btn" aria-label="Меню" @click="navOpen = !navOpen">
          <i class="pi pi-bars"></i>
        </button>
        <span class="mobilebar__title">{{ title }}</span>
        <button
          v-if="hasRight"
          class="mobilebar__btn"
          aria-label="Действия"
          @click="asideOpen = !asideOpen"
        >
          <i class="pi pi-sliders-h"></i>
        </button>
      </div>

      <div class="shell__scroll">
        <RouterView />
      </div>
    </main>

    <!-- ПРАВАЯ: действия над контентом (опционально) -->
    <aside v-if="hasRight" class="shell__aside">
      <div class="shell__scroll shell__scroll--aside">
        <RouterView name="right" />
      </div>
    </aside>

    <!-- Затемнение под мобильные шторки -->
    <div class="scrim" @click="closeDrawers"></div>
  </div>
</template>

<style scoped>
.shell {
  height: 100vh;
  display: grid;
  grid-template-columns: 248px minmax(0, 1fr);
  background-color: var(--background);
  color: var(--text);
}
.shell--has-right {
  grid-template-columns: 248px minmax(0, 1fr) 320px;
}

.shell__sidebar {
  min-width: 0;
  min-height: 0;
}

.shell__center {
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border-inline: 1px solid var(--border);
}

.shell__aside {
  min-width: 0;
  min-height: 0;
  background-color: var(--surface-sunken);
}

/* Прокручиваемая область */
.shell__scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 0.75rem;
  scrollbar-gutter: stable;
}
.shell__scroll--aside {
  height: 100%;
}

.shell__center .shell__scroll {
  margin-inline-end: 0.35rem;
  padding-inline-end: 0.55rem;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in srgb, var(--accent) 36%, transparent) transparent;
}
.shell__center .shell__scroll:hover {
  scrollbar-color: color-mix(in srgb, var(--accent) 62%, transparent) transparent;
}
.shell__center .shell__scroll::-webkit-scrollbar {
  width: 8px;
}
.shell__center .shell__scroll::-webkit-scrollbar-track {
  background: transparent;
}
.shell__center .shell__scroll::-webkit-scrollbar-thumb {
  min-height: 44px;
  border: 2px solid transparent;
  border-radius: 999px;
  background-color: color-mix(in srgb, var(--accent) 36%, transparent);
  background-clip: content-box;
}
.shell__center .shell__scroll:hover::-webkit-scrollbar-thumb {
  background-color: color-mix(in srgb, var(--accent) 62%, transparent);
}
.shell__center .shell__scroll::-webkit-scrollbar-thumb:hover {
  background-color: var(--accent);
}

/* Мобильная шапка — скрыта на десктопе */
.mobilebar { display: none; }
.mobilebar__btn {
  font: inherit;
  cursor: pointer;
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 2px solid var(--border);
  background: var(--surface-raised);
  color: var(--text);
}
.mobilebar__btn:active { transform: scale(0.96); }

.scrim { display: none; }

/* ============ Мобильная адаптация ============ */
@media (max-width: 960px) {
  .shell {
    grid-template-columns: 1fr;
  }
  .shell--has-right {
    grid-template-columns: 1fr;
  }

  .shell__center {
    border-inline: 0;
  }

  .mobilebar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid var(--border);
    background-color: var(--brand-deep);
    color: var(--brand-text);
    position: sticky;
    top: 0;
    z-index: 3;
  }
  .mobilebar__title {
    flex: 1;
    font-weight: 700;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Сайдбар и правая панель становятся выезжающими шторками */
  .shell__sidebar,
  .shell__aside {
    position: fixed;
    top: 0;
    bottom: 0;
    width: 256px;
    z-index: 20;
    transition: transform 0.28s ease;
  }
  .shell__sidebar {
    left: 0;
    transform: translateX(-102%);
    box-shadow: 2px 0 16px var(--shadow);
  }
  .shell__aside {
    right: 0;
    width: 280px;
    transform: translateX(102%);
    box-shadow: -2px 0 16px var(--shadow);
    border-left: 1px solid var(--border);
  }
  .is-nav-open .shell__sidebar { transform: translateX(0); }
  .is-aside-open .shell__aside { transform: translateX(0); }

  .is-nav-open .scrim,
  .is-aside-open .scrim {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 15;
    background-color: color-mix(in srgb, #000 40%, transparent);
  }
}

@media (prefers-reduced-motion: reduce) {
  .shell__sidebar,
  .shell__aside { transition: none; }
}
</style>
