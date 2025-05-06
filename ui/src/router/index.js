import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/category/:category',
      name: 'category',
      component: () => import('../views/CategoryView.vue')
    },
    {
      path: '/api/:apiName',
      name: 'api-detail',
      component: () => import('../views/ApiDetailView.vue')
    },
    {
      path: '/api-registry',
      name: 'api-registry',
      component: () => import('../views/ApiRegistryView.vue')
    }
  ]
})

export default router 