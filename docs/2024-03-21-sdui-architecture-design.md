# SDUI架构设计决策

**日期**: 2024-03-21
**类别**: 架构设计
**紧急程度**: 高

## 设计决策

### 1. 架构模式选择

采用"固定框架 + 动态内容"的分离式架构模式：

- 固定框架：包含顶部导航、左侧菜单等固定结构
- 动态内容：基于JSON配置的页面内容动态渲染

### 2. 核心配置结构

```json
{
  "menus": [
    {
      "id": "moduleId",
      "title": "模块名称",
      "icon": "icon-name",
      "children": [
        {
          "id": "pageId",
          "title": "页面名称",
          "path": "/path/to/page",
          "pageKey": "uniquePageKey"
        }
      ]
    }
  ],
  
  "pages": {
    "uniquePageKey": {
      "type": "page",
      "version": "1.0",
      "properties": {
        "title": "页面标题",
        "layout": "standard",
        "components": []
      }
    }
  }
}
```

### 3. 动态加载机制

- 菜单配置：应用启动时一次性加载
- 页面配置：按需动态加载
- 配置缓存：支持本地缓存和版本控制

## 待分析事项

### 1. 组件系统设计

- [ ] 基础组件类型清单
- [ ] 组件属性标准化
- [ ] 组件间通信机制
- [ ] 组件扩展机制
- [ ] 组件样式主题支持

### 2. 数据绑定方案

- [ ] 数据源定义格式
- [ ] 数据绑定表达式语法
- [ ] 双向绑定实现
- [ ] 数据联动机制
- [ ] 数据验证规则

### 3. 后端响应机制

- [ ] 配置存储方案
- [ ] API接口设计
- [ ] 数据聚合服务
- [ ] 权限控制
- [ ] 缓存策略

### 4. 开发支持

- [ ] 配置开发工具
- [ ] 调试能力支持
- [ ] 测试方案
- [ ] 文档生成
- [ ] 版本管理

### 5. 性能优化

- [ ] 配置加载优化
- [ ] 渲染性能优化
- [ ] 缓存策略
- [ ] 按需加载
- [ ] 资源预加载

## 下一步计划

1. 细化组件系统设计
   - 定义核心组件集
   - 设计组件属性规范
   - 实现示例组件

2. 实现数据绑定方案
   - 设计数据绑定语法
   - 开发绑定解析器
   - 实现数据流转机制

3. 开发基础框架
   - 实现配置加载器
   - 开发渲染引擎
   - 集成路由系统

## 风险评估

1. 技术风险
   - 组件扩展的复杂性
   - 性能优化的挑战
   - 配置维护的成本

2. 业务风险
   - 学习成本
   - 开发效率
   - 维护难度

## 相关资源

- 技术栈：FastAPI, Vue3, TypeScript
- 参考项目：
  - Ant Design Pro
  - Vue Admin
  - React Admin

## 注意事项

1. 保持配置简单性
2. 注重开发体验
3. 重视性能优化
4. 完善错误处理
5. 做好版本兼容

## 具体约定

### 1. 应用框架约定

```typescript
// 应用框架接口定义
interface AppFramework {
  // 固定框架结构
  layout: {
    header: {
      height: number;      // 头部高度
      fixed: boolean;      // 是否固定
      components: {        // 固定组件
        logo: LogoComponent;
        userInfo: UserInfoComponent;
        globalSearch?: SearchComponent;
      };
    };
    sider: {
      width: number;       // 侧边栏宽度
      collapsible: boolean;// 是否可折叠
      theme: 'light' | 'dark'; // 主题
    };
    content: {
      padding: number;     // 内容区内边距
      tabMode: 'multi' | 'single'; // 标签页模式
    };
  };
  
  // 全局状态
  state: {
    user: UserState;
    theme: ThemeState;
    permissions: string[];
  };
}
```

### 2. 页面配置约定

```typescript
// 页面配置接口
interface PageConfig {
  pageKey: string;        // 页面唯一标识
  version: string;        // 配置版本号
  title: string;         // 页面标题
  permissions?: string[]; // 页面权限
  
  // 页面布局
  layout: {
    type: 'standard' | 'custom' | 'blank';
    header?: {
      title?: string;
      breadcrumb?: boolean;
      actions?: ActionConfig[];
    };
  };
  
  // 页面状态定义
  state?: {
    [key: string]: {
      type: 'string' | 'number' | 'boolean' | 'object' | 'array';
      default?: any;
      persist?: boolean;  // 是否持久化
    };
  };
  
  // 数据源定义
  dataSources?: {
    [key: string]: {
      type: 'api' | 'static' | 'compute';
      api?: string;
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
      params?: Record<string, any>;
      transform?: string; // 数据转换表达式
      cache?: {
        enabled: boolean;
        duration: number;
      };
    };
  };
  
  // 组件配置
  components: ComponentConfig[];
}

// 组件配置接口
interface ComponentConfig {
  type: string;          // 组件类型
  id: string;           // 组件ID
  props?: Record<string, any>; // 组件属性
  
  // 数据绑定
  bindings?: {
    [prop: string]: {
      type: 'state' | 'dataSource' | 'compute';
      source: string;    // 数据源或状态键
      transform?: string; // 转换表达式
    };
  };
  
  // 事件处理
  events?: {
    [event: string]: {
      type: 'api' | 'state' | 'navigate';
      action: string;    // 动作定义
      params?: Record<string, any>;
    }[];
  };
  
  // 条件渲染
  condition?: {
    when: string;       // 条件表达式
    otherwise?: ComponentConfig; // 替代组件
  };
  
  // 子组件
  children?: ComponentConfig[];
}
```

### 3. 数据绑定表达式约定

1. **状态绑定**

```json
{
  "bindings": {
    "value": {
      "type": "state",
      "source": "formData.name"
    }
  }
}
```

1. **数据源绑定**

```json
{
  "bindings": {
    "options": {
      "type": "dataSource",
      "source": "storeList",
      "transform": "item => ({ label: item.name, value: item.id })"
    }
  }
}
```

1. **计算表达式**

```json
{
  "bindings": {
    "disabled": {
      "type": "compute",
      "source": "!state.formData.type || state.loading"
    }
  }
}
```

### 4. 组件通信约定

1. **父子通信**

```json
{
  "events": {
    "onChange": [{
      "type": "state",
      "action": "setState",
      "params": {
        "path": "formData.name",
        "value": "$event"
      }
    }]
  }
}
```

1. **跨组件通信**

```json
{
  "events": {
    "onClick": [{
      "type": "broadcast",
      "action": "refreshTable",
      "params": {
        "force": true
      }
    }]
  }
}
```

### 5. 权限控制约定

```json
{
  "permissions": {
    "page": ["product.view"],
    "components": {
      "editButton": ["product.edit"],
      "deleteButton": ["product.delete"]
    }
  }
}
```

### 6. 生命周期约定

```json
{
  "lifecycle": {
    "onMount": [
      {
        "type": "dataSource",
        "action": "load",
        "target": ["storeList", "categoryList"]
      }
    ],
    "onUnmount": [
      {
        "type": "state",
        "action": "clear",
        "target": "formData"
      }
    ]
  }
}
```
