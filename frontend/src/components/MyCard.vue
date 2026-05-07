<script lang="ts" setup>
import { Card,Button} from 'primevue';
import { useToast } from 'primevue/usetoast';
const toast = useToast();


const show = () => {
    toast.add({ severity: 'info', summary: 'Не имплементировано', detail: 'Вы должны заменить Кнопку на свою', life: 3000 });
};

</script>

<template>
    <Card class="custom-card">
        <template #content>
            <template class="flex w-full">

                <div class="flex-1">
                <slot name="content"></slot>

                </div>
                <div class="flex-none content-end">
                    <slot name="buttons">
                        <Button v-on:click="show" size="small" severity="info">
                            <i class="pi pi-info"></i>
                        </Button>
                    </slot>
                </div>


            </template>

 
        </template>

        <template #subtitle>
            <slot name="subtitle">
                
            </slot>
        </template>

    </Card>

</template>


<style scoped>
/* Стили для самого контейнера карты */
.custom-card {
    text-align: left;
    background-color: #f6d6bd;
    border: 2.5px solid #927878;
    color : #826373;
}


.custom-card:hover {
    background-color: rgb(233, 215, 203);
}

/* Стили для внутреннего контента PrimeVue Card */
.custom-card :deep(.p-card-content) {
    padding: 0; /* Убираем стандартные отступы */
    color: #373737;
}
</style>