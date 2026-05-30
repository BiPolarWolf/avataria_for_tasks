<script lang='ts' setup>
import { ref } from 'vue'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';
import MyTextInput from '@/components/inputs/MyTextInput.vue';
import MySelect from '@/components/inputs/MySelect.vue';

const data = ref({
    title : '',
    text : '',
    importans : 1,
    tag_ids : []
})

const tagsApiUrl = 'tags/'

const success_function = () =>{
    data.value = {
    title : '',
    text : '',
    importans : 1,
    tag_ids : []
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

    <MySelect 
    option-label="text"
    option-value="id"
    v-model="data.tag_ids" multiple :api-url="tagsApiUrl" label="Теги"></MySelect>

    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>