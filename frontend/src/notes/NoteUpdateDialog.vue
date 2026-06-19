<script lang='ts' setup>
import { reactive, watch } from "vue";
import MyDialog from '@/components/MyDialog.vue';
import MyForm from '@/components/MyForm.vue';
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';
import MySelect from "@/components/inputs/MySelect.vue";
import MyTextInput from "@/components/inputs/MyTextInput.vue";
interface NoteUpdatePayload {
    id: number
    title : string
    text: string
    importans: number
    tag_ids: any[]
}

interface NoteUpdateInitial {
    id: number
    title : string
    text: string
    importans: number
    tags : any[]
}



const visible = defineModel<boolean>('visible', { default: false })
const initial = defineModel<NoteUpdateInitial | null>('initial', { default: null })

const data = reactive<NoteUpdatePayload>({
    id: 0,
    title : '',
    text: '',
    importans: 1,
    tag_ids: [],
})

const tagsApiUrl = 'tags/'

const fillForm = (note: NoteUpdateInitial | null) => {
    if (!note) {
        data.id = 0
        data.title = ''
        data.text = ''
        data.importans = 1
        data.tag_ids = []
        
        return
    }

    console.log(note)

    data.id = note.id
    data.title = note.title
    data.text = note.text
    data.tag_ids = note.tags.map(note => note.id)
}

watch(
    () => initial.value,
    (task) => {
        fillForm(task)
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
        :mutated_keys_list="['notes']"
        success_message="Запись обновлена"
        title="Обновить запись"
        url="notes/update" 
    >   
        <MyTextInput
        v-model="data.title"
        label="Заголовок"
        ></MyTextInput>

        <MyTextArea
            v-model="data.text"
            label="Описание"
            placeholder="Например: как прошел мой день"
        />
        <MyRatingInput v-model="data.importans" label="Важность" />

        <MySelect 
            option-label="text"
            option-value="id"
            v-model="data.tag_ids" multiple :api-url="tagsApiUrl" label="Теги"></MySelect>

    </MyForm>
</MyDialog>
</template>

<style scoped>
</style>
