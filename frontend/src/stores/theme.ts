import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import {
  DEFAULT_THEME_ID,
  getTheme,
  themeToVars,
} from '@/theme/themes'

const STORAGE_KEY = 'themeId'

/**
 * Стор тем.
 *  - применяет только базовые смысловые токены (6 цветов + шрифт) на :root;
 *  - оттенки (hover/brand/тень и т.п.) считает CSS в theme/tokens.css, а не JS;
 *  - набор ключей фиксирован → не нужен сброс «чужих» переменных при смене темы.
 */
export const useThemeStore = defineStore('theme', () => {
  const currentId = ref<string>(localStorage.getItem(STORAGE_KEY) ?? DEFAULT_THEME_ID)

  function apply(id: string) {
    const vars = themeToVars(getTheme(id))
    const root = document.documentElement
    // Набор ключей одинаков у всех тем, поэтому просто перезаписываем их все.
    for (const [key, value] of Object.entries(vars)) {
      root.style.setProperty(key, value)
    }
  }

  function setTheme(id: string) {
    currentId.value = id
  }

  watch(
    currentId,
    (id) => {
      apply(id)
      localStorage.setItem(STORAGE_KEY, id)
    },
    { immediate: true },
  )

  return { currentId, setTheme }
})
