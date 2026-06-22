import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useSettingsStore = defineStore('settings', () => {

  // 1. Инициализируем state.
  // Читаем из localStorage, если там пусто — ставим false по умолчанию.
  // Важно: localStorage хранит всё в виде строк, поэтому используем JSON.parse()
  const savedShowNotes = localStorage.getItem('showNotesText')
  const showNotesText = ref(savedShowNotes ? JSON.parse(savedShowNotes) : false)

  // 2. Настраиваем слежение (watch)
  // При каждом изменении showNotesText новое значение будет улетать в localStorage
  watch(showNotesText, (newValue) => {
    localStorage.setItem('showNotesText', JSON.stringify(newValue))
  })

  // actions (действия)
  function showNotesTextSwitcher(){
    showNotesText.value = !showNotesText.value
  }

  return {
    showNotesText,
    showNotesTextSwitcher
  }
})