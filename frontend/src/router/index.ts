import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/Home.vue'
import About from '@/About.vue'

const routes = [
    {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    component: About
  },
  {
    path: '/tasks',
    name: 'tasks',
    // Ленивая загрузка (компонент подгрузится только при переходе)
    component: () => import('../tasks/TaskTabs.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    // Ленивая загрузка (компонент подгрузится только при переходе)
    component: () => import('../account/Profile.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../account/Login.vue')
  }
]

const router = createRouter({
  history: createWebHistory(), // Чистые URL без # (например, /about вместо /#/about)
  routes
})

export default router