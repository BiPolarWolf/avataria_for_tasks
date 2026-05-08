<script lang='ts' setup>
import { reactive, watch } from "vue";
import MyDialog from '@/components/MyDialog.vue';
import MyForm from '@/components/MyForm.vue';
import MyTextArea from '@/components/inputs/MyTextArea.vue';
import MyRatingInput from '@/components/inputs/MyRatingInput.vue';

interface TaskUpdatePayload {
    id: number
    description: string
    complexity: number
    status: boolean
}

const visible = defineModel<boolean>('visible', { default: false })
const initial = defineModel<TaskUpdatePayload | null>('initial', { default: null })

const data = reactive<TaskUpdatePayload>({
    id: 0,
    description: '',
    complexity: 1,
    status: false,
})

const fillForm = (task: TaskUpdatePayload | null) => {
    if (!task) {
        data.id = 0
        data.description = ''
        data.complexity = 1
        data.status = false
        return
    }

    data.id = task.id
    data.description = task.description
    data.complexity = task.complexity
    data.status = task.status
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
        :mutated_keys_list="['tasks']"
        success_message="Задача обновлена"
        title="Обновить задачу"
        url="tasks/update" 
    >
        <MyTextArea
            v-model="data.description"
            label="Описание"
            placeholder="Например: пройти ежедневные задания и собрать награды"
        />
        <MyRatingInput v-model="data.complexity" label="Сложность" />
    </MyForm>
</MyDialog>
</template>

<style scoped>
</style>
