import '../public/assets/main.css'
import { createApp } from 'vue'
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import ToastService from 'primevue/toastservice';
import { VueQueryPlugin } from '@tanstack/vue-query';
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/index'


const pinia = createPinia()
const app = createApp(App)


app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});


app.use(router) // Подключаем роутер
app.use(pinia) 
app.use(ToastService)
app.use(VueQueryPlugin)
app.mount('#app')
