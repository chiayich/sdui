# SDUI前端实施 - 第一阶段

**日期**: 2024-03-21
**类别**: 前端开发
**阶段**: Phase 1 - 基础框架搭建

## 实施目标

1. 创建项目基础结构
2. 实现框架核心定义
3. 完成基础页面渲染
4. 支持Mock数据展示

## 项目结构

```bash
src/
├── assets/           # 静态资源
├── components/       # 通用组件
│   ├── basic/       # 基础组件
│   └── business/    # 业务组件
├── core/            # 核心实现
│   ├── framework/   # 框架实现
│   ├── renderer/    # 渲染引擎
│   └── types/       # 类型定义
├── layouts/         # 布局组件
│   ├── AppLayout.vue    # 应用布局
│   └── components/      # 布局相关组件
├── pages/           # 页面组件
├── router/          # 路由配置
├── services/        # 服务封装
│   ├── api/         # API服务
│   └── mock/        # Mock数据
├── stores/          # 状态管理
└── utils/           # 工具函数
```

## 核心实现步骤

### 1. 框架核心定义

```typescript
// src/core/types/framework.ts
export interface AppConfig {
  layout: LayoutConfig;
  router: RouterConfig;
  state: StateConfig;
}

export interface LayoutConfig {
  header: HeaderConfig;
  sider: SiderConfig;
  content: ContentConfig;
}

// src/core/framework/app.ts
export class SDUIApp {
  private config: AppConfig;
  private renderer: SDUIRenderer;
  
  constructor(config: AppConfig) {
    this.config = config;
    this.renderer = new SDUIRenderer();
  }
  
  async bootstrap() {
    // 1. 初始化框架
    // 2. 加载配置
    // 3. 启动应用
  }
}
```

### 2. 渲染引擎实现

```typescript
// src/core/renderer/index.ts
export class SDUIRenderer {
  private componentRegistry: ComponentRegistry;
  
  constructor() {
    this.componentRegistry = new ComponentRegistry();
  }
  
  async render(pageConfig: PageConfig) {
    // 1. 解析配置
    // 2. 加载组件
    // 3. 渲染页面
  }
}
```

### 3. 状态管理设计

```typescript
// src/stores/framework.ts
export const useFrameworkStore = defineStore('framework', {
  state: () => ({
    pageConfigs: {} as Record<string, PageConfig>,
    currentPage: null as string | null,
  }),
  
  actions: {
    async loadPageConfig(pageKey: string) {
      // 1. 检查缓存
      // 2. 加载配置
      // 3. 更新状态
    }
  }
});
```

## Mock数据结构

### 1. 菜单配置

```json
{
  "menus": [
    {
      "id": "product",
      "title": "商品通",
      "icon": "ShoppingOutlined",
      "children": [
        {
          "id": "product-flow",
          "title": "商品流通工作台",
          "path": "/product/flow",
          "pageKey": "productFlow"
        }
      ]
    }
  ]
}
```

### 2. 页面配置

```json
{
  "pageKey": "productFlow",
  "version": "1.0",
  "title": "商品流通工作台",
  "layout": {
    "type": "standard",
    "header": {
      "title": "商品流通工作台",
      "breadcrumb": true
    }
  },
  "components": [
    {
      "type": "filterBar",
      "id": "mainFilter",
      "props": {
        "items": [
          {
            "type": "select",
            "props": {
              "label": "DAZZLE",
              "placeholder": "请选择"
            }
          }
        ]
      }
    },
    {
      "type": "table",
      "id": "mainTable",
      "props": {
        "columns": [
          {
            "title": "需求单号",
            "dataIndex": "orderNo"
          }
        ]
      }
    }
  ]
}
```

## 设计边界

### 1. 渲染边界

- 只处理JSON配置定义的UI结构
- 不处理复杂的业务逻辑
- 不处理数据处理逻辑

### 2. 组件边界

- 只支持预定义的组件类型
- 组件间通信通过事件机制
- 不支持自定义渲染函数

### 3. 数据边界

- 只支持简单的数据绑定
- 复杂数据处理在后端完成
- 状态管理只处理UI状态

## 下一步计划

1. 实现基础组件库
2. 完善渲染引擎
3. 添加数据绑定支持
4. 实现事件处理机制

## 注意事项

1. 保持代码简洁清晰
2. 注重类型定义完整性
3. 考虑性能优化空间
4. 做好错误处理
5. 保留扩展性 