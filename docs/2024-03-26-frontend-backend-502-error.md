# SDUI前端访问后端API 502网关错误

**日期**: 2024-03-26
**类别**: 前端/后端
**紧急程度**: 高

## 问题描述

在宿主机上无法访问部署后的前端页面，前端与后端API通信时出现502网关错误。此问题导致前端应用无法获取UI配置数据，影响了整个SDUI框架的核心功能。

## 问题分析

经过排查，发现以下几个可能的问题原因：

1. **前端API调用配置问题**：前端代码中没有正确的API调用模块，使用了模拟数据而不是真实API调用
2. **环境变量配置**：前端应用没有正确获取API服务器的URL配置
3. **网络连接问题**：容器网络与宿主机之间存在连接问题
4. **CORS配置**：后端API没有正确配置跨域资源共享
5. **路由匹配问题**：前端尝试访问的API端点与后端路由不匹配

通过检查发现，后端服务已正常运行（可以通过curl在容器内访问API），但前端没有正确的API调用实现。

## 解决思路

针对上述问题，我们采取以下解决方案：

1. 创建标准化的API工具模块，负责处理与后端的所有通信
2. 实现Pinia状态管理库，处理UI配置的管理和缓存
3. 确保环境变量正确配置，使前端能够连接到后端API
4. 优化错误处理，提供用户友好的错误提示
5. 更新前端组件，使用实际API替代模拟数据

## 执行步骤

1. 创建API工具模块，处理与后端的通信：

```typescript
// frontend/src/lib/api.ts
import axios from 'axios';

// 从环境变量获取API基础URL
const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// 创建axios实例
const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 响应拦截器处理错误
apiClient.interceptors.response.use(
  response => response.data,
  error => {
    let message = '请求失败';
    if (error.response) {
      const status = error.response.status;
      switch (status) {
        case 502:
          message = '网关错误，请检查API服务是否正常运行';
          break;
        // 其他错误处理...
      }
    }
    return Promise.reject({ message, originalError: error });
  }
);

// API方法封装
export const uiTemplatesApi = {
  getScreenConfig: async (screenId, context = {}) => {
    try {
      return await apiClient.get(`/api/ui-templates/${screenId}`, { params: context });
    } catch (error) {
      throw error;
    }
  }
};
```

2. 创建Pinia状态管理，处理UI配置：

```typescript
// frontend/src/stores/uiStore.ts
import { defineStore } from 'pinia';
import api from '../lib/api';

export const useUIStore = defineStore('ui', {
  state: () => ({
    screens: {},
    loading: false,
    error: null,
    currentScreenId: null
  }),
  
  getters: {
    currentScreen: (state) => {
      if (!state.currentScreenId) return null;
      return state.screens[state.currentScreenId] || null;
    },
    isLoading: (state) => state.loading,
    errorMessage: (state) => state.error
  },
  
  actions: {
    async loadScreen(screenId, forceRefresh = false) {
      this.loading = true;
      this.error = null;
      
      try {
        const screenConfig = await api.uiTemplates.getScreenConfig(screenId);
        this.screens[screenId] = screenConfig;
        this.currentScreenId = screenId;
        return screenConfig;
      } catch (error) {
        this.error = error.message;
        throw error;
      } finally {
        this.loading = false;
      }
    }
  }
});
```

3. 更新前端视图组件，使用Pinia存储：

```vue
<!-- frontend/src/views/SDUIView.vue -->
<template>
  <div class="sdui-view">
    <div v-if="uiStore.isLoading" class="loading">
      <p>Loading UI configuration...</p>
    </div>
    
    <div v-else-if="uiStore.errorMessage" class="error">
      <h2>Error Loading UI</h2>
      <p>{{ uiStore.errorMessage }}</p>
      <button @click="handleRetry">Retry</button>
    </div>
    
    <div v-else-if="uiConfig" class="renderer-container">
      <h1>{{ uiConfig.screen?.title || 'SDUI Screen' }}</h1>
      <div class="component-placeholder">
        <pre>{{ JSON.stringify(uiConfig, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUIStore } from '../stores/uiStore';

const route = useRoute();
const uiStore = useUIStore();
const screenId = computed(() => route.params.screenId as string);
const uiConfig = computed(() => uiStore.currentScreen);

const loadScreen = async (forceRefresh = false) => {
  try {
    await uiStore.loadScreen(screenId.value, forceRefresh);
  } catch (error) {
    console.error('Failed to load screen:', error);
  }
};

const handleRetry = () => {
  loadScreen(true);
};

watch(screenId, () => loadScreen());
onMounted(() => loadScreen());
</script>
```

4. 创建TypeScript环境变量声明文件：

```typescript
// frontend/src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_PORT: string;
  readonly VITE_HOST: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

## 结果验证

要验证问题是否已解决，可以执行以下步骤：

1. 在容器内重新启动前端开发服务器：
   ```bash
   cd frontend && ./restart-dev.sh
   ```

2. 在宿主机浏览器中访问：
   ```
   http://localhost:5173
   ```

3. 检查前端是否能成功加载UI配置：
   - 如果页面正常加载，则表示问题已解决
   - 如果仍然出现502错误，可以查看浏览器控制台中的详细错误信息

## 相关资源

- [前端API工具模块](../frontend/src/lib/api.ts)
- [Pinia UI存储模块](../frontend/src/stores/uiStore.ts)
- [SDUI视图组件](../frontend/src/views/SDUIView.vue)
- [环境变量类型定义](../frontend/src/vite-env.d.ts)
- [Axios文档](https://axios-http.com/docs/intro)
- [Pinia文档](https://pinia.vuejs.org/)

## 注意事项

1. 确保宿主机能够访问容器暴露的端口
2. 如果使用HTTPS，需要处理混合内容问题
3. 如果后端API路径变更，需要同步更新前端API工具模块
4. 在生产环境中，应使用正确的API基础URL和环境变量
5. 考虑在生产环境中实现更复杂的错误处理和重试机制 