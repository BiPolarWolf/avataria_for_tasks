<script lang='ts' setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';

const router = useRouter()

const data = ref({
    description : '',
    complexity : 1
})


const success_function = () =>{
    data.value = {
    description : '',
    complexity : 1
    }
    // После создания возвращаемся к списку задач.
    router.push({ name: 'tasks' })
}

</script>

<template>

    <MyForm 
        title="Создать новую задачу"
        :data="data" 
        url="tasks/create" 
        :success_function="success_function" 
        :mutated_keys_list="['tasks']"
    
    >

    <MyTextArea
    :is_restricted="true"
    v-model="data.description" label="Описание" placeholder="Например: пройти ежедневные задания и собрать награды"></MyTextArea>

    <MyRatingInput v-model="data.complexity" label="Сложность"></MyRatingInput>

    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>