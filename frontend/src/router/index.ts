import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/Home.vue'
import About from '@/About.vue'
import Settings from '@/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Главная' },
  },
  {
    path: '/about',
    component: About,
    meta: { title: 'О проекте' },
  },
  {
    path: '/settings',
    component: Settings,
    meta: { title: 'Настройки' },
  },
  {
    path: '/notes',
    name: 'notes',
    meta: { title: 'Записи' },
    // Центр = список, правая = действия (кнопка «Создать»)
    components: {
      default: () => import('../notes/NoteList.vue'),
      right: () => import('../notes/NotesListAside.vue'),
    },
  },
  {
    path: '/notes/create',
    name: 'notes-create',
    meta: { title: 'Новая запись' },
    // Центр = форма во всю ширину, правая = кнопка «Вернуться»
    components: {
      default: () => import('../notes/NoteCreate.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      right: {
        to: 'notes',
        eyebrow: 'Новая запись',
        hint: 'Заполни форму в центре и сохрани — вернёшься к списку записей.',
      },
    },
  },
  {
    path: '/notes/:id/edit',
    name: 'notes-edit',
    meta: { title: 'Редактирование записи' },
    // Центр = форма редактирования, правая = кнопка «Вернуться»
    components: {
      default: () => import('../notes/NoteEdit.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      default: true, // id из URL передаётся как prop
      right: { to: 'notes', eyebrow: 'Редактирование записи' },
    },
  },
  {
    path: '/tags',
    name: 'tags',
    meta: { title: 'Теги' },
    // Центр = список, правая = действия (кнопка «Создать»)
    components: {
      default: () => import('../tags/TagsList.vue'),
      right: () => import('../tags/TagsListAside.vue'),
    },
  },
  {
    path: '/tags/create',
    name: 'tags-create',
    meta: { title: 'Новый тег' },
    // Центр = форма во всю ширину, правая = кнопка «Вернуться»
    components: {
      default: () => import('../tags/TagCreate.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      right: {
        to: 'tags',
        eyebrow: 'Новый тег',
        hint: 'Заполни форму в центре и сохрани — вернёшься к списку тегов.',
      },
    },
  },
  {
    path: '/tags/:id/edit',
    name: 'tags-edit',
    meta: { title: 'Редактирование тега' },
    // Центр = форма редактирования, правая = кнопка «Вернуться»
    components: {
      default: () => import('../tags/TagEdit.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      default: true, // id из URL передаётся как prop
      right: { to: 'tags', eyebrow: 'Редактирование тега' },
    },
  },
  {
    path: '/tasks',
    name: 'tasks',
    meta: { title: 'Задачи' },
    // Центр = список с переключателем статуса, правая = действия
    components: {
      default: () => import('../tasks/TaskList.vue'),
      right: () => import('../tasks/TasksListAside.vue'),
    },
  },
  {
    path: '/tasks/create',
    name: 'tasks-create',
    meta: { title: 'Новая задача' },
    // Центр = форма во всю ширину, правая = кнопка «Вернуться»
    components: {
      default: () => import('../tasks/TaskCreate.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      right: {
        to: 'tasks',
        eyebrow: 'Новая задача',
        hint: 'Заполни форму в центре и сохрани — вернёшься к списку задач.',
      },
    },
  },
  {
    path: '/tasks/:id/edit',
    name: 'tasks-edit',
    meta: { title: 'Редактирование задачи' },
    // Центр = форма редактирования, правая = кнопка «Вернуться»
    components: {
      default: () => import('../tasks/TaskEdit.vue'),
      right: () => import('../components/BackAside.vue'),
    },
    props: {
      default: true, // id из URL передаётся как prop
      right: { to: 'tasks', eyebrow: 'Редактирование задачи' },
    },
  },
  {
    path: '/profile',
    name: 'profile',
    meta: { title: 'Профиль' },
    component: () => import('../account/Profile.vue'),
  },
  {
    path: '/login',
    name: 'login',
    meta: { title: 'Вход' },
    component: () => import('../account/Login.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(), // Чистые URL без # (например, /about вместо /#/about)
  routes,
})

export default router
