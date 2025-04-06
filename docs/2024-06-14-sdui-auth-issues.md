# SDUI API认证问题修复

**日期**: 2024-06-14
**类别**: 前端
**紧急程度**: 高

## 问题描述

前端应用在获取SDUI配置时出现401 Unauthorized错误，控制台显示"GET http://localhost:5173/api/sdui/structure 401 (Unauthorized)"。尽管auth store已经成功安装，但SDUI API请求未能正确携带认证令牌。

## 问题分析

分析日志和代码后，发现以下几个问题：

1. SDUI API服务使用了独立的axios实例（sduiApi），该实例虽然配置了请求拦截器从localStorage获取token，但与应用其他部分使用的全局axios实例是分开的
2. 应用初始化时，auth store的initAuth方法负责设置全局axios请求头的Authorization，但这不会影响到单独创建的axios实例
3. App.vue中的loadStructure方法在组件挂载时立即调用，可能在auth store完成初始化之前就开始发送请求
4. 没有处理未认证状态下加载公共资源的逻辑

## 解决思路

1. 修改SDUI API服务，使用全局axios实例而不是创建新实例，确保共享相同的认证配置
2. 修改App.vue中的loadStructure方法，在发起请求前先检查认证状态
3. 确保App.vue在挂载时等待auth store初始化完成后再加载结构
4. 添加未认证状态下的处理逻辑，可以尝试加载公共资源或重定向到登录页面

## 执行步骤

1. 修改SDUI API服务，使用全局axios实例：

```typescript
// frontend/src/api/sdui.ts
import axios from 'axios';

// 接口类型定义
export interface SDUIConfig {
    id: string;
    type: string;
    title?: string;
    is_public?: boolean;
    content?: any[];
    styles?: Record<string, any>;
    scripts?: Record<string, any>;
    [key: string]: any;
}

// SDUI接口服务
export const sduiService = {
    /**
     * 获取页面配置
     * @param configCode - 配置代码
     */
    getConfig: async (configCode: string): Promise<SDUIConfig> => {
        const response = await axios.get(`/api/sdui/${configCode}`);
        return response.data;
    },
    
    /**
     * 获取公共页面配置（无需认证）
     * @param configCode - 配置代码
     */
    getPublicConfig: async (configCode: string): Promise<SDUIConfig> => {
        const response = await axios.get(`/api/sdui/public/${configCode}`);
        return response.data;
    }
};

export default sduiService;
```

2. 修改App.vue以在加载结构前检查认证状态：

```typescript
// frontend/src/App.vue
import { ref, reactive, onMounted, watch } from 'vue';
import axios from 'axios';
import { useAuthStore } from './stores/authStore';
import NavMenu from '@/components/NavMenu.vue';
import ComponentRenderer from '@/components/sdui/ComponentRenderer.vue';

// 系统结构状态
const isLoading = ref(false);
const error = ref<string | null>(null);
const structureLoaded = ref(false);
const navigationConfig = ref(null);
const globalComponents = ref<any[]>([]);
const globalContext = reactive({
  user: null,
  theme: 'light',
  // 其他全局状态
});

// 获取认证状态
const authStore = useAuthStore();

// 加载系统结构配置
const loadStructure = async () => {
  isLoading.value = true;
  error.value = null;

  // 如果未认证，等待一段时间再检查认证状态
  if (!authStore.isAuthenticated) {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 如果仍未认证，则重定向到登录页面或加载公共结构
    if (!authStore.isAuthenticated) {
      console.warn('User not authenticated, loading public structure');
      try {
        const response = await axios.get('/api/sdui/public/structure');
        navigationConfig.value = response.data.navigation;
        globalComponents.value = response.data.global_components || [];
        structureLoaded.value = true;
      } catch (err: any) {
        console.error('Failed to load public structure:', err);
        error.value = err.response?.data?.detail || '加载系统结构失败';
      } finally {
        isLoading.value = false;
      }
      return;
    }
  }

  try {
    const response = await axios.get('/api/sdui/structure');
    navigationConfig.value = response.data.navigation;
    globalComponents.value = response.data.global_components || [];
    structureLoaded.value = true;

    // 获取用户信息已在auth store中处理，直接使用
    globalContext.user = authStore.user;
  } catch (err: any) {
    console.error('Failed to load application structure:', err);
    error.value = err.response?.data?.detail || '加载系统结构失败';
  } finally {
    isLoading.value = false;
  }
};

// 组件挂载时加载系统结构
onMounted(async () => {
  // 等待auth store初始化完成
  if (authStore.isLoading) {
    await new Promise(resolve => {
      const unwatch = watch(() => authStore.isLoading, (loading) => {
        if (!loading) {
          unwatch();
          resolve(true);
        }
      });
    });
  }
  
  loadStructure();
});
```

3. 确认main.ts中已正确初始化auth store：

```typescript
// frontend/src/main.ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './assets/main.css'
import { useAuthStore } from './stores/authStore'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')

// 初始化认证状态
const authStore = useAuthStore()
authStore.initAuth()
```

## 结果验证

1. 重启开发服务器
2. 使用浏览器开发者工具网络面板观察API请求
3. 验证认证正确时SDUI API请求携带了Authorization请求头
4. 验证未认证时是否能正确处理公共资源的获取
5. 确认控制台不再显示401 Unauthorized错误

## 相关资源

- [frontend/src/api/sdui.ts](src/api/sdui.ts)
- [frontend/src/App.vue](src/App.vue)
- [frontend/src/stores/authStore.ts](src/stores/authStore.ts)
- [frontend/src/api/auth.ts](src/api/auth.ts)

## 注意事项

- 确保后端API正确实现了公共和私有资源的区分
- 此修复使SDUI服务依赖于全局axios配置，如果其他部分代码修改了axios.defaults.headers，可能会影响SDUI服务
- 考虑在路由守卫中添加认证检查，以便在未认证时自动重定向到登录页面 