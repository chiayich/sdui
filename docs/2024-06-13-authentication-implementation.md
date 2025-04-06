# 认证系统实现

**日期**: 2024-06-13  
**类别**: 前端/安全  
**紧急程度**: 高

## 问题描述

系统需要实现完整的用户认证功能，以确保应用安全和用户身份验证。当前应用没有独立的登录页面和认证状态管理，导致用户无法安全访问受保护的资源。需要开发一个独立的Vue登录组件，并将其与现有的路由系统和后端API集成。

## 问题分析

应用的认证系统需要解决以下关键问题：

1. **用户界面**: 需要一个独立的登录页面，不依赖于SDUI配置，以确保登录功能始终可用
2. **状态管理**: 需要维护用户认证状态，包括令牌存储和用户信息
3. **路由保护**: 需要防止未认证用户访问受保护的路由
4. **API集成**: 需要与后端认证API进行集成
5. **用户体验**: 需要提供清晰的登录/登出流程和错误处理

认证系统是应用安全的核心组件，需要确保实现的安全性和可靠性。

## 解决思路

采用以下方案实现认证系统：

1. **前端架构**:
   - 创建独立的Vue登录组件和视图
   - 使用Pinia进行状态管理
   - 实现路由守卫进行认证检查

2. **认证流程**:
   - 用户输入凭据 → 发送到后端 → 获取令牌 → 存储令牌 → 获取用户信息 → 更新状态

3. **安全考虑**:
   - 使用JWT令牌
   - 令牌存储在localStorage中
   - 为API请求添加Authorization头

## 执行步骤

### 1. 创建认证API服务

创建`frontend/src/api/auth.ts`文件，实现与后端认证API的交互：

```typescript
import axios from 'axios';

// 定义类型
export interface LoginPayload {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserInfoResponse {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  roles?: Array<{ id: number, name: string }>;
  permissions?: string[];
}

// 创建认证API服务
const authService = {
  login: async (payload: LoginPayload): Promise<LoginResponse> => {
    const response = await axios.post('/api/v1/login/access-token', payload);
    return response.data;
  },
  
  getUserInfo: async (token: string): Promise<UserInfoResponse> => {
    const response = await axios.get('/api/v1/users/me', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  },
  
  saveToken: (token: string): void => {
    localStorage.setItem('auth_token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  },
  
  clearToken: (): void => {
    localStorage.removeItem('auth_token');
    delete axios.defaults.headers.common['Authorization'];
  },
  
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('auth_token');
  }
};

export default authService;
```

### 2. 实现认证状态管理

创建`frontend/src/stores/authStore.ts`文件，使用Pinia管理认证状态：

```typescript
import { defineStore } from 'pinia';
import authService, { UserInfoResponse } from '@/api/auth';

interface AuthState {
  token: string | null;
  user: UserInfoResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('auth_token'),
    user: null,
    isAuthenticated: !!localStorage.getItem('auth_token'),
    isLoading: false,
    error: null
  }),

  actions: {
    async login(username: string, password: string) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await authService.login({ username, password });
        this.token = response.access_token;
        authService.saveToken(response.access_token);
        this.isAuthenticated = true;
        await this.fetchUserInfo();
        return true;
      } catch (error: any) {
        this.error = error.response?.data?.detail || '登录失败';
        return false;
      } finally {
        this.isLoading = false;
      }
    },
    
    logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      authService.clearToken();
    },
    
    async fetchUserInfo() {
      if (!this.token) return;
      
      try {
        const userInfo = await authService.getUserInfo(this.token);
        this.user = userInfo;
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    
    initAuth() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        this.token = token;
        this.isAuthenticated = true;
        authService.saveToken(token);
        this.fetchUserInfo();
      }
    }
  }
});
```

### 3. 创建登录页面组件

创建`frontend/src/views/LoginView.vue`文件：

```vue
<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">登录系统</h1>
      
      <div class="alert error" v-if="authStore.error">
        {{ authStore.error }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="credentials.username" required />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="credentials.password" required />
        </div>
        
        <div class="form-group check">
          <input type="checkbox" id="remember" v-model="credentials.remember" />
          <label for="remember">记住我</label>
        </div>
        
        <div class="form-group">
          <button type="submit" class="login-button" :disabled="authStore.isLoading">
            <span v-if="authStore.isLoading">登录中...</span>
            <span v-else>登录</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
const router = useRouter();

const credentials = ref({
  username: '',
  password: '',
  remember: false
});

const handleLogin = async () => {
  const success = await authStore.login(
    credentials.value.username,
    credentials.value.password
  );
  
  if (success) {
    router.push('/');
  }
};
</script>
```

### 4. 更新路由配置

修改`frontend/src/router/index.ts`文件，添加登录路由和路由守卫：

```typescript
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    // 其他路由配置
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    // ...
  ]
});

// 添加全局前置守卫
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth !== false;
  const isAuthenticated = !!localStorage.getItem('auth_token');

  // 如果需要认证但未登录，重定向到登录页面
  if (requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } 
  // 如果已登录且试图访问登录页，重定向到首页
  else if (isAuthenticated && to.name === 'login') {
    next({ name: 'home' });
  } 
  // 其他情况正常导航
  else {
    next();
  }
});

export default router;
```

### 5. 更新主应用入口

修改`frontend/src/main.ts`，初始化认证状态：

```typescript
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/authStore';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.use(router);

app.mount('#app');

// 初始化认证状态
const authStore = useAuthStore();
authStore.initAuth();
```

## 结果验证

实施上述步骤后，进行以下验证：

1. **登录功能验证**:
   - 打开应用，确认未登录用户被重定向到登录页面
   - 使用有效凭据登录，验证是否成功获取令牌并跳转到首页
   - 使用无效凭据登录，验证是否显示正确的错误信息

2. **认证状态验证**:
   - 登录后刷新页面，确认用户仍然保持登录状态
   - 检查localStorage是否正确存储了令牌
   - 验证API请求是否包含正确的Authorization头

3. **路由保护验证**:
   - 尝试在未登录状态下访问受保护路由，确认是否重定向到登录页面
   - 登录后访问受保护路由，确认能够正常访问
   - 已登录状态下尝试访问登录页面，确认是否重定向到首页

## 相关资源

- [Vue Router文档](https://router.vuejs.org/)
- [Pinia文档](https://pinia.vuejs.org/)
- [JWT认证最佳实践](https://auth0.com/blog/jwt-authentication-best-practices/)

## 注意事项

1. 在生产环境中，应考虑使用HTTPS确保令牌传输安全
2. 令牌应设置合理的过期时间，并实现刷新令牌机制
3. 考虑在后续版本中实现Remember Me功能的完整支持
4. 敏感操作应要求用户二次认证
5. 应实现用户活动超时自动登出机制 