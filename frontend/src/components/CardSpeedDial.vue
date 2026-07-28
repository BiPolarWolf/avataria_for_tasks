<script setup lang="ts">
import SpeedDial from 'primevue/speeddial'

export interface CardSpeedDialItem {
  label: string
  icon: string
  command: () => void
  severity?: 'info' | 'success' | 'danger' | 'secondary' | 'primary'
  disabled?: boolean
}

interface Props {
  items: CardSpeedDialItem[]
  direction?: 'up' | 'down' | 'left' | 'right'
  ariaLabel?: string
}

withDefaults(defineProps<Props>(), {
  direction: 'left',
  ariaLabel: 'Действия',
})
</script>

<template>
  <!-- Обёртка, а не сам SpeedDial: у него inheritAttrs: false, поэтому
       scope-id scoped-стилей до его корня не доходит. -->
  <div class="card-speeddial">
    <SpeedDial
      :model="items"
      :direction="direction"
      type="linear"
      :transition-delay="60"
      show-icon="pi pi-ellipsis-v"
      hide-icon="pi pi-times"
      :rotate-animation="false"
      hide-on-click-outside
      button-class="ui-btn ui-btn--icon dial-btn"
      :aria-label="ariaLabel"
    >
      <template #item="{ item, onClick }">
        <button
          type="button"
          class="ui-btn ui-btn--icon dial-btn"
          :class="`dial-btn--${item.severity ?? 'secondary'}`"
          :disabled="!!item.disabled"
          :title="String(item.label ?? '')"
          :aria-label="String(item.label ?? '')"
          @click="onClick"
        >
          <i :class="item.icon"></i>
        </button>
      </template>
    </SpeedDial>
  </div>
</template>

<style scoped>
/* Дайл живёт в потоке, отдельной строкой снизу карточки: вне потока он
   ложился поверх контента и перекрывал теги. */
.card-speeddial {
  display: flex;
  justify-content: flex-end;
}

/* Обвязка у всех кнопок дайла одна и та же — форма, бордер, тень.
   Действия различаются только оттенком --dial-tint (заливка и иконка),
   поэтому глобальные ui-btn--* здесь не используются: у них бордер
   свой на каждую severity, от почти чёрного до цвета текста. */
.card-speeddial :deep(.dial-btn) {
  --dial-tint: var(--muted);
  --ui-btn-border: var(--border);
  --ui-btn-border-hover: var(--border-strong);
  --ui-btn-bg-top: color-mix(in srgb, var(--dial-tint) 10%, var(--surface-raised));
  --ui-btn-bg-bottom: color-mix(in srgb, var(--dial-tint) 18%, var(--surface-sunken));
  --ui-btn-bg-top-hover: color-mix(in srgb, var(--dial-tint) 20%, var(--surface-raised));
  --ui-btn-bg-bottom-hover: color-mix(in srgb, var(--dial-tint) 28%, var(--surface-sunken));
  /* Подмешиваем текст темы: иконка остаётся читаемой и на светлом, и на тёмном. */
  --ui-btn-text: color-mix(in srgb, var(--dial-tint) 65%, var(--text));
  width: 2.4rem;
  height: 2.4rem;
}

.card-speeddial :deep(.dial-btn--info),
.card-speeddial :deep(.dial-btn--primary) {
  --dial-tint: var(--accent);
}

.card-speeddial :deep(.dial-btn--success) {
  --dial-tint: #6f9f5f;
}

.card-speeddial :deep(.dial-btn--danger) {
  --dial-tint: #c0503c;
}
</style>
