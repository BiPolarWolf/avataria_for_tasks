<script lang='ts' setup>
import { ref } from 'vue'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';
import MyTextInput from '@/components/inputs/MyTextInput.vue';

const data = ref({
    title : '',
    text : '',
    importans : 1
})


const success_function = () =>{
    data.value = {
    title : '',
    text : '',
    importans : 1
    }
}

</script>

<template>

    <MyForm 
        title="Создать новую запись"
        :data="data" 
        url="notes/create/" 
        :success_function="success_function" 
        :mutated_keys_list="['notes']"
    >

    <MyTextInput v-model="data.title" label="Заголовок" ></MyTextInput>

    <MyTextArea 
        :is_restricted="true" 
        v-model="data.text" 
        label="Описание" 
        placeholder="Например: как прошел мой день"
    ></MyTextArea>

    <MyRatingInput v-model="data.importans" :max="10" label="Важность"></MyRatingInput>

    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>