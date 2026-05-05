import '../public/assets/main.css'
import { createApp } from 'vue'
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import ToastService from 'primevue/toastservice';



import App from './App.vue'
import router from './router/index'

const app = createApp(App)


app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(router) // Подключаем роутер
app.use(ToastService)
app.mount('#app')
