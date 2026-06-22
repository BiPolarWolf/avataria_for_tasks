<script lang='ts' setup>
import { useSettingsStore } from './stores/settings';
import MyButton from './components/MyButton.vue';
import { storeToRefs } from 'pinia'


const settingsStore = useSettingsStore()

const { showNotesText} = storeToRefs(settingsStore)

const {showNotesTextSwitcher} = settingsStore


</script>

<template>

    <div class="setting_tab">
    <p> Показывать текст в списке записей в вкладке "Записи"</p> 

    <MyButton @click="showNotesTextSwitcher" type="button">
        {{ showNotesText ? 'Скрыть' : 'Показать' }}
    </MyButton>
    </div>



</template>

<style scoped>

.setting_tab{
    background-color: var(--color-paper-500);
    border: 5px solid var(--color-paper-700);
    padding: 2em;

}

.setting_tab p {
    display: block;
    padding-bottom : 1em
}

</style>