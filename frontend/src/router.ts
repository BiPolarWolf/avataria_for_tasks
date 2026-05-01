import { createMemoryHistory, createRouter } from 'vue-router'

import Profile from './account/Profile.vue'
import Login from './account/Login.vue'

const routes = [
  { path: '/me', component: Profile },
  { path: '/login', component: Login },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})