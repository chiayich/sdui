import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SDUIView from '@/views/SDUIView.vue';
import LoginView from '@/views/LoginView.vue';

// 系统管理路由
const systemRoutes = [
    {
        path: '/system',
        name: 'System',
        component: () => import('@/pages/sdui/SystemPage.vue'),
        meta: {
            title: '系统管理',
            requiresAuth: true,
            permissions: ['system:view']
        }
    },
    {
        path: '/system/organization',
        name: 'Organization',
        component: () => import('@/pages/sdui/OrganizationPage.vue'),
        meta: {
            title: '组织架构管理',
            requiresAuth: true,
            permissions: ['organization:view']
        }
    },
    {
        path: '/system/role',
        name: 'Role',
        component: () => import('@/pages/sdui/RolePage.vue'),
        meta: {
            title: '角色权限管理',
            requiresAuth: true,
            permissions: ['role:view']
        }
    },
    {
        path: '/system/user',
        name: 'User',
        component: () => import('@/pages/sdui/UserPage.vue'),
        meta: {
            title: '用户管理',
            requiresAuth: true,
            permissions: ['user:view']
        }
    },
    {
        path: '/system/config',
        name: 'Config',
        component: () => import('@/pages/sdui/ConfigPage.vue'),
        meta: {
            title: '系统配置',
            requiresAuth: true,
            permissions: ['config:view']
        }
    }
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
            meta: {
                requiresAuth: false
            }
        },
        {
            path: '/about',
            name: 'about',
            // 懒加载
            component: () => import('../views/AboutView.vue'),
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/sdui/:screenId',
            name: 'sdui',
            component: SDUIView,
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/logs',
            name: 'logs',
            component: () => import('../views/LogsView.vue'),
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/flow/instruction',
            name: 'Instruction',
            component: SDUIView,
            props: {
                schema: '/api/sdui/instruction'
            },
            meta: {
                requiresAuth: true
            }
        },
        {
            path: '/flow/simulation',
            name: 'Simulation',
            component: SDUIView,
            props: {
                schema: '/api/sdui/simulation'
            },
            meta: {
                requiresAuth: true
            }
        },
        ...systemRoutes
    ]
})

// 全局导航守卫
router.beforeEach((to, from, next) => {
    // 获取存储的token
    const token = localStorage.getItem('auth_token');

    // 检查路由是否需要认证
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

    if (requiresAuth && !token) {
        // 需要认证但没有token，重定向到登录页
        next({ name: 'login' });
    } else if (to.name === 'login' && token) {
        // 已有token但访问登录页，直接跳转到首页
        next({ name: 'home' });
    } else {
        // 继续导航
        next();
    }
})

export default router 