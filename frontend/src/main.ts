import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import { useAuthStore } from './stores/authStore'
import { useSduiStore } from './stores/sduiStore'
import api from './axios-config'

// 导入axios并使用新的axios配置
import axios from 'axios'

// 设置全局默认值
axios.defaults.baseURL = api.defaults.baseURL
axios.defaults.timeout = api.defaults.timeout

// 添加拦截器 - 请求拦截
axios.interceptors.request.use(
    config => {
        // 从本地获取认证令牌并添加到请求头
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }

        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 添加拦截器 - 响应拦截
axios.interceptors.response.use(
    response => response,
    error => {
        // 处理401错误 - 未授权
        if (error.response && error.response.status === 401) {
            console.log('拦截到401错误，重定向到登录页');
            localStorage.removeItem('auth_token');
            router.push('/login');
        }

        return Promise.reject(error);
    }
);

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// 增强的应用初始化流程，确保首先加载系统结构与目录
const initializeApp = async () => {
    console.log('开始应用初始化流程');

    // 初始化认证状态
    const authStore = useAuthStore();
    await authStore.initAuth();

    // 确保认证初始化完成后再初始化SDUI
    const sduiStore = useSduiStore();

    try {
        console.log('初始化SDUI状态');
        await sduiStore.initialize();

        // 如果已经认证并且结构尚未加载，强制加载结构
        if (authStore.isAuthenticated && !sduiStore.isStructureLoaded) {
            console.log('用户已认证但结构未加载，开始加载系统结构');
            await sduiStore.loadStructure();
        }

        console.log('SDUI状态初始化完成', {
            已认证: authStore.isAuthenticated,
            结构已加载: sduiStore.isStructureLoaded,
            导航菜单项: sduiStore.navigationConfig?.menuItems?.length || 0
        });
    } catch (err) {
        console.error('SDUI初始化失败:', err);
    }

    console.log('应用初始化完成');

    // 最后挂载应用
    app.mount('#app');
};

// 执行初始化
initializeApp().catch(error => {
    console.error('应用初始化失败:', error);
    // 即使初始化出错也挂载应用，以便显示错误信息
    app.mount('#app');
}); 