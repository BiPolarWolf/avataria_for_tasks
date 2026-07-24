<script lang='ts' setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MyForm from '@/components/MyForm.vue'
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';
import MyTextInput from '@/components/inputs/MyTextInput.vue';
import MySelect from '@/components/inputs/MySelect.vue';

const router = useRouter()

const data = ref({
    title : '',
    description : '',
    complexity : 1,
    tag_ids : [] as number[]
})

const tagsApiUrl = 'tags/'

const success_function = () =>{
    data.value = {
    title : '',
    description : '',
    complexity : 1,
    tag_ids : []
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

    <MyTextInput v-model="data.title" label="Заголовок (необязательно)"></MyTextInput>

    <MyTextArea
    :is_restricted="true"
    v-model="data.description" label="Описание" placeholder="Например: пройти ежедневные задания и собрать награды"></MyTextArea>

    <MyRatingInput v-model="data.complexity" label="Сложность"></MyRatingInput>

    <MySelect
    option-label="text"
    option-value="id"
    v-model="data.tag_ids" multiple :api-url="tagsApiUrl" label="Теги"></MySelect>

    <!-- {{ data }} -->

    </MyForm>

</template>

<style scoped>
</style>
