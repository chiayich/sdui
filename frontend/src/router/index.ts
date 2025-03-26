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
            path: '/about',
            name: 'about',
            // 懒加载
            component: () => import('../views/AboutView.vue')
        },
        {
            path: '/sdui/:screenId',
            name: 'sdui',
            component: () => import('../views/SDUIView.vue')
        },
        {
            path: '/logs',
            name: 'logs',
            component: () => import('../views/LogsView.vue')
        }
    ]
})

export default router 