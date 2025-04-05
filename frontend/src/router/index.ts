import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SDUIPage from '@/views/SDUIPage.vue';
import { mockHomeConfig } from '@/services/mock/home-config';
import { mockSimulationConfig } from '@/services/mock/simulation-config';

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
        },
        {
            path: '/flow/instruction',
            name: 'Instruction',
            component: SDUIPage,
            props: {
                config: mockHomeConfig
            }
        },
        {
            path: '/flow/simulation',
            name: 'Simulation',
            component: SDUIPage,
            props: {
                config: mockSimulationConfig
            }
        }
    ]
})

export default router 