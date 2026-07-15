<script lang="ts" setup>
import { Card } from 'primevue';
import { useToast } from 'primevue/usetoast';
import MyButton from './MyButton.vue';
const toast = useToast();


const show = () => {
    toast.add({ severity: 'info', summary: 'Не имплементировано', detail: 'Вы должны заменить Кнопку на свою', life: 3000 });
};

</script>

<template>
    <Card class="custom-card">


        <template #subtitle>
            <slot name="subtitle">
                
            </slot>
        </template>


        <template #content>
            <slot name="content"></slot>
        </template>

        <template #footer>

            <div class="actions">
            <slot name="actions" class="actions">
                <MyButton v-on:click="show" size="small" severity="info">
                            <i class="pi pi-info"></i>
                </MyButton>
            </slot>
            </div>
        </template>

    </Card>

</template>


<style scoped>
/* Стили для самого контейнера карты */
.custom-card {
    text-align: left;
    background-color: var(--surface);
    border: 2.5px solid var(--border);
    color : var(--muted);
}

.actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
}


.custom-card:hover {
    background-color: var(--surface-raised);
}

/* Стили для внутреннего контента PrimeVue Card */
.custom-card :deep(.p-card-content) {
    padding: 0; /* Убираем стандартные отступы */
    color: var(--text);
}
</style>
