<script lang='ts' setup>
import { reactive, watch } from "vue";
import MyDialog from '@/components/MyDialog.vue';
import MyForm from '@/components/MyForm.vue';
import MyTextInput from "@/components/inputs/MyTextInput.vue";
import MyColorPicker from "@/components/inputs/MyColorPicker.vue";
import DeleteConfirmButton from "@/components/DeleteConfirmButton.vue";
import TagUntieButton from "./TagUntieButton.vue";

interface TagUpdatePayload {
    id: number
    text: string
    color: string
}

const visible = defineModel<boolean>('visible', { default: false })
const initial = defineModel<TagUpdatePayload | null>('initial', { default: null })

const data = reactive<TagUpdatePayload>({
        id: 0,
        text: '',
        color: '#EAD7BB',
})

const fillForm = (tag: TagUpdatePayload | null) => {
    if (!tag) {
        data.id = 0
        data.text = ''
        data.color = '#EAD7BB'
        return
    }

    data.id = tag.id
    data.text = tag.text
    data.color = tag.color
}

watch(
    () => initial.value,
    (tag) => {
        fillForm(tag)
    },
    { immediate: true }
)

const closeDialog = () => {
    visible.value = false
    initial.value = null
    fillForm(null)
}

const success_function = () =>{
    closeDialog()
}

</script>

<template>
<MyDialog
    v-model:visible="visible"
    modal
    :style="{ width: '50rem' }"
    @hide="closeDialog"
>
    <MyForm 
        :success_function="success_function" 
        :data="data" 
        :mutated_keys_list="['tags']"
        success_message="Тег обновлён"
        title="Обновить тег"
        url="tags/update" 
    >

    <MyTextInput v-model="data.text" label="Название" />

    <MyColorPicker v-model="data.color" label="Цвет" />

    <template #other_buttons>

        <TagUntieButton :tag-id="data.id" :tag-text="data.text" />

        <DeleteConfirmButton  :query-key="'tags'" :object_id="data.id"></DeleteConfirmButton>        
    </template>

    </MyForm>
    
</MyDialog>
</template>

<style scoped>
</style>
