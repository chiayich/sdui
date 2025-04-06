# 前端SDUI Mock数据迁移到后端数据库

**日期**: 2024-06-14
**类别**: 前端/后端
**紧急程度**: 中

## 问题描述

前端组件中的SDUI mock数据直接硬编码在代码中，需要迁移到后端数据库，以便更灵活地管理和更新配置数据。前端代码中存在对本地mock数据的直接引用，导致无法直接从后端获取配置数据。

## 问题分析

在SDUIRenderer.vue组件中，存在对本地mock数据文件的直接引入：
```javascript
import { mockStores, mockRecentOrders } from '@/services/mock/data';
```

这些mock数据被用于本地测试和开发，但现在需要从后端数据库获取这些数据，以确保前后端数据一致性，并支持动态更新配置。

## 解决思路

1. 创建一个专门的SDUI API服务，负责与后端通信获取配置数据
2. 修改SDUIRenderer.vue组件，删除本地mock数据的引用
3. 将getDataSource方法改为异步方法，从后端API获取数据
4. 处理组件渲染中的异步数据加载问题

## 执行步骤

1. 创建前端SDUI API服务文件

```typescript
// src/api/sdui.ts
import axios from 'axios';

const sduiApi = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 为所有请求添加认证令牌
sduiApi.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

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
    const response = await sduiApi.get(`/api/sdui/${configCode}`);
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

2. 修改SDUIRenderer.vue，移除mock数据导入

```typescript
// 移除这一行
import { mockStores, mockRecentOrders } from '@/services/mock/data';
// 添加SDUI服务导入
import { sduiService } from '@/api/sdui';
```

3. 将getDataSource方法改为异步方法

```typescript
// 获取数据源
const getDataSource = async (source: string): Promise<any[]> => {
  // 如果缓存中有数据，直接返回
  if (dataSourceCache.value[source]) {
    return dataSourceCache.value[source];
  }

  // 从后端API获取数据
  try {
    const response = await sduiService.getConfig(`data/${source}`);
    const data = response.content || [];
    
    // 缓存数据
    dataSourceCache.value[source] = data;
    return data;
  } catch (error) {
    console.error(`Error fetching data source ${source}:`, error);
    return [];
  }
};
```

4. 修改resolveBinding和resolveProps方法处理异步数据

```typescript
// 解析绑定值
const resolveBinding = async (binding: any) => {
  if (!binding) return null;
  
  switch (binding.type) {
    case 'state':
      return pageState.value[binding.source];
    case 'dataSource':
      try {
        return await getDataSource(binding.source);
      } catch (error) {
        console.error(`Error resolving binding for ${binding.source}:`, error);
        return [];
      }
    case 'compute':
      // 这里可以添加计算属性的支持
      return null;
    default:
      return null;
  }
};

// 解析组件属性
const resolveProps = async (component: any) => {
  const props = { ...component.props };
  
  // 处理数据绑定
  if (component.bindings) {
    for (const [key, binding] of Object.entries(component.bindings)) {
      props[key] = await resolveBinding(binding);
    }
  }
  
  return props;
};
```

5. 创建异步组件包装器，处理组件的异步数据加载

```typescript
// 创建异步组件包装器
const AsyncComponent = defineComponent({
  props: {
    componentType: {
      type: [String, Object],
      required: true
    },
    componentData: {
      type: Object,
      required: true
    }
  },
  emits: ['state-change'],
  data() {
    return {
      resolvedProps: {},
      loading: true,
      error: null as Error | null
    };
  },
  async created() {
    try {
      this.loading = true;
      this.resolvedProps = await resolveProps(this.componentData);
      this.loading = false;
    } catch (err: any) {
      this.error = err instanceof Error ? err : new Error(String(err));
      this.loading = false;
      console.error('Error resolving props:', err);
    }
  },
  render() {
    if (this.loading) {
      return h('div', { class: 'loading-component' }, '加载中...');
    }
    
    if (this.error) {
      return h('div', { class: 'error-component' }, `加载出错: ${this.error.message}`);
    }
    
    const events = resolveEvents(this.componentData);
    
    return h(this.componentType, {
      ...this.resolvedProps,
      ...events
    });
  }
});
```

6. 修改模板中的组件渲染部分

```html
<!-- 将原来的组件渲染 -->
<component
  :is="resolveComponent(component.type)"
  v-bind="resolveProps(component)"
  v-on="resolveEvents(component)"
/>

<!-- 替换为异步组件 -->
<AsyncComponent
  :component-type="resolveComponent(component.type)"
  :component-data="component"
  @state-change="(key, value) => emit('state-change', key, value)"
/>
```

## 结果验证

1. 启动前端开发服务器，确认没有控制台错误
2. 检查页面是否正常加载和显示从后端获取的数据
3. 验证数据更新功能是否正常工作

## 相关资源

- [frontend/src/core/components/SDUIRenderer.vue](frontend/src/core/components/SDUIRenderer.vue)
- [frontend/src/api/sdui.ts](frontend/src/api/sdui.ts)
- [frontend/src/services/mock/data.ts](frontend/src/services/mock/data.ts)

## 注意事项

- 确保后端API已经准备好，支持根据数据源名称获取相应的数据
- 需要为所有现有的mock数据在数据库中创建对应的配置记录
- 前端的缓存机制应谨慎使用，需要考虑数据更新时的刷新策略 