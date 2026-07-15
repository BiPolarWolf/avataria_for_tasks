<script lang='ts' setup>
import { useSettingsStore } from './stores/settings';
import { useThemeStore } from './stores/theme';
import { THEMES } from './theme/themes';
import MyButton from './components/MyButton.vue';
import { storeToRefs } from 'pinia'


const settingsStore = useSettingsStore()
const { showNotesText } = storeToRefs(settingsStore)
const { showNotesTextSwitcher } = settingsStore

const themeStore = useThemeStore()
// currentId реактивен (ref) — берём через storeToRefs.
const { currentId } = storeToRefs(themeStore)
const { setTheme } = themeStore
// presets — статичный список, берём прямо из модуля.
const presets = THEMES
</script>

<template>

    <div class="setting_tab">
        <p>Тема оформления</p>

        <div class="theme-grid">
            <button
                v-for="preset in presets"
                :key="preset.id"
                type="button"
                class="theme-card"
                :class="{ 'theme-card--active': preset.id === currentId }"
                @click="setTheme(preset.id)"
            >
                <span class="theme-swatch">
                    <span
                        v-for="(color, i) in [preset.colors.background, preset.colors.surface, preset.colors.accent]"
                        :key="i"
                        class="theme-swatch__color"
                        :style="{ backgroundColor: color }"
                    />
                </span>
                <span class="theme-card__label">{{ preset.label }}</span>
            </button>
        </div>
    </div>

    <div class="setting_tab">
        <p> Показывать текст в списке записей в вкладке "Записи"</p>

        <MyButton @click="showNotesTextSwitcher" type="button">
            {{ showNotesText ? 'Скрыть' : 'Показать' }}
        </MyButton>
    </div>

</template>

<style scoped>

.setting_tab{
    background-color: var(--surface);
    color: var(--text);
    border: 5px solid var(--border);
    padding: 2em;
    margin-bottom: 1em;
}

.setting_tab p {
    display: block;
    padding-bottom : 1em
}

.theme-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
}

.theme-card {
    display: flex;
    flex-direction: column;
    gap: 0.5em;
    padding: 0.75em;
    cursor: pointer;
    background: var(--surface-raised);
    border: 3px solid var(--border);
    color: var(--text);
    font-family: var(--font-body);
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}

.theme-card:hover {
    transform: translateY(-1px);
    box-shadow: 3px 3px 0 var(--shadow);
}

.theme-card--active {
    border-color: var(--accent);
    box-shadow: 3px 3px 0 var(--shadow);
}

.theme-swatch {
    display: flex;
    width: 6rem;
    height: 2.5rem;
    border: 2px solid var(--border-strong);
}

.theme-swatch__color {
    flex: 1;
}

.theme-card__label {
    font-size: 0.9rem;
    text-align: center;
}

</style>
