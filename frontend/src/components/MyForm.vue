<script lang='ts' setup>
import axios from 'axios';
import { useMutation, useQueryClient } from '@tanstack/vue-query';
import { useToast } from 'primevue/usetoast';
import MyButton from './MyButton.vue';

interface Props {
  title?: string;
  data: any;
  url : string;
  mutated_keys_list ?: string[];
  success_function : Function;
  success_message ?: string ;
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Заголовок по умолчанию',
  success_message : 'Данные успешно обновились',
})

const toast = useToast()
const queryClient = useQueryClient()


async function inner_post_handler(data:any){

    const token = localStorage.getItem('access_token')
    if (!token) {
        throw new Error('Сначала войдите в аккаунт')
    }
    const response = await axios.post(`http://localhost:8000/${props.url}`, data, {
        headers: { Authorization: `Bearer ${token}`}
    })
    return response.data

}

const { mutate, isPending } = useMutation({
  mutationFn: inner_post_handler,
  onSuccess: async (returnedData) => { // Сервер присылает созданный объект
    // 1. Обновляем кэш
    await queryClient.invalidateQueries({ queryKey: props.mutated_keys_list ? props.mutated_keys_list : [] })
    
    // 2. Показываем радостный тост
    toast.add({
      severity: 'success',
      summary: 'Успех!',
      detail: props.success_message,
      life: 3000
    })

    // 3. Выполняем колбэк (например, закрытие модалки)
    props.success_function(returnedData)
  },
  onError: (error: any) => {
    // Вытаскиваем сообщение из ответа FastAPI
    const errorDetail = error.response?.data?.detail
    
    // Если FastAPI вернул ошибку валидации Pydantic (массив ошибок)
    if (Array.isArray(errorDetail)) {
       errorDetail.forEach(err => {
         toast.add({ 
            severity: 'error', 
            summary: 'Ошибка валидации', 
            detail: `${err.loc[1]}: ${err.msg}`,
            life: 5000 })
       })
    } else {
      toast.add({
        severity: 'error',
        summary: 'Ошибка',
        detail: errorDetail || 'Что-то пошло не так',
        life: 3000
      })
    }
  }
})


function submit(){
  mutate(props.data)
}

</script>

<template>

<form class="form_class" @submit.prevent="submit">

    <div class="form_title text-xl ">
        <slot name="title">{{ props.title }}</slot>
    </div>

    <hr>

    <div class="form_inputs">
        <slot>Тут будут Inputs</slot>
    </div>

    <hr>

    <div class="form_buttons">
        <slot name="buttons" :isPendind="isPending">
            <MyButton type="submit" :disabled="isPending" severity="success">
                {{ isPending ? 'Сохраняется...' : 'Сохранить' }} <img src="@/assets/icons/FloppyDisk.png" width="18px" alt="">
            </MyButton>
        </slot>
    </div>

</form>


</template>

<style scoped>

hr{
    background-color:  var(--color-paper-500); 
    color : var(--color-paper-500);
    padding: 2px 0px;
}

.form_class{
    background-color: var(--color-paper-400);
    border: 5px solid var(--color-paper-700);
    color: var(--color-secondary-900) ;
}

.form_title{
    padding: 1em;
    
}

.form_inputs{
    padding: 1em;
}

.form_buttons{
    padding: 1em;
}

</style>
