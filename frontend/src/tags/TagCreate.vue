<script lang='ts' setup>
import { ref } from 'vue'
import MyForm from '@/components/MyForm.vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue';
import MyColorPicker from '@/components/inputs/MyColorPicker.vue';

const data = ref({
    text : '',
    color : '#EAD7BB',
})


const success_function = () =>{
    data.value = {
        text : '',
        color : '#EAD7BB',
    }
}

</script>

<template>

    <MyForm 
        title="Создать новый тег"
        :data="data" 
        url="tags/create" 
        :success_function="success_function" 
        :mutated_keys_list="['tags']"
    >

            <MyTextInput v-model="data.text" label="Название"></MyTextInput>
            <MyColorPicker v-model="data.color" label="Цвет"></MyColorPicker>


    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>
