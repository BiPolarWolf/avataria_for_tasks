<script lang='ts' setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MyForm from '@/components/MyForm.vue'
import MyTextInput from '@/components/inputs/MyTextInput.vue';
import MyColorPicker from '@/components/inputs/MyColorPicker.vue';

const router = useRouter()

const data = ref({
    text : '',
    color : '#EAD7BB',
})


const success_function = () =>{
    data.value = {
        text : '',
        color : '#EAD7BB',
    }
    // После создания возвращаемся к списку тегов.
    router.push({ name: 'tags' })
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
