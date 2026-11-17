import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AddApplicationView from '../views/AddApplicationView.vue'
import VerifyApplicationView from '../views/VerifyApplicationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/add',
      name: 'add',
      component: AddApplicationView
    },
    {
      path: '/verify/:id', // :id означает, что мы будем передавать номер заявки в URL
      name: 'verify',
      component: VerifyApplicationView
    }
  ]
})

export default router