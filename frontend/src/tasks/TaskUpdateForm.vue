<script lang='ts' setup>
import { ref } from 'vue'
import MyForm from '@/components/MyForm.vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue';

const data = ref({test:''})


const success_function = () =>{
    alert('test')
}

</script>

<template>

    <MyForm 
        :data="data" 
        url="tasks/create/" 
        :success_function="success_function" 
    >

    <MyTextInput v-model="data.test" label="Тестовое поле" error="Поле обязательно к заполнению"></MyTextInput>


    </MyForm>

</template>

<style scoped>
</style>