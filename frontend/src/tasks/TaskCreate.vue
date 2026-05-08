<script lang='ts' setup>
import { ref } from 'vue'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';

const data = ref({
    description : '',
    complexity : 1
})




const success_function = () =>{
    data.value = {
    description : '',
    complexity : 1
    }
}

</script>

<template>

    <MyForm 
        :data="data" 
        url="tasks/create/" 
        :success_function="success_function" 
        :mutated_keys_list="['tasks']"
    
    >

    <MyTextArea v-model="data.description" label="Описание" placeholder="Например: пройти ежедневные задания и собрать награды"></MyTextArea>

    <MyRatingInput v-model="data.complexity" label="Сложность"></MyRatingInput>

    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>