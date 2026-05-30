<script lang='ts' setup>
import {Tab, TabPanel, Tabs, TabList} from 'primevue';

interface Props {
  tabs: {value:string,title:string}[]
  default_value : string
}

const props = defineProps<Props>()

</script>

<template>
    <Tabs class="custom_tabs" :value="default_value">
        <TabList class="custom_tablist">
            <Tab v-for="tab in tabs" :key="tab.value" :value="tab.value" >{{ tab.title }}</Tab>
        </TabList>
        <TabPanels>
            <TabPanel class="custom_tabpanel" v-for="tab in tabs" :key="tab.value" :value="tab.value">
                <div class="p-3 text-white">
                    <slot  :name="tab.value"> "{{ tab.title }}" не заполнен </slot>
                </div>
            </TabPanel>
        </TabPanels>
    </Tabs>
</template>

<style scoped>

.custom_tabs {
    width: 100%;
    min-width: 0;
}

.custom_tabpanel {
    width: 100%;
}

.custom_tablist :deep(.p-tab-active){
    color: var(--color-secondary-100);
    /* background-color: var(--color-primary); */
    background-color: var(--color-secondary-600);
    
     
}

.custom_tablist :deep(.p-tablist-active-bar){
    background-color: white;
}

.custom_tablist{
    width: calc(100% - 20px);
    box-sizing: border-box;
    background-color: var(--color-primary-200);
    border: 8px solid var(--color-primary-400);
    margin : 10px;

}

.custom_tablist :deep(.p-tablist-tab-list) {
    display: flex;
    width: 100%;
    border-width: 0px !important;
    border-color: red;
}

.custom_tablist :deep(.p-tab) {
    flex: 1 1 0;
    min-width: 0;
    justify-content: center;
    text-align: center;
    white-space: normal;
}

.custom_tablist :deep(.p-tablist-active-bar) {
    transition: transform 0.15s ease, width 0.15s ease;
}

</style>



