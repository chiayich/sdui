# Vite TypeScript ImportMeta.env错误修复

**日期**: 2025-03-26
**类别**: 前端
**紧急程度**: 中

## 问题描述

在SDUI前端项目中，TypeScript报错"Property 'env' does not exist on type 'ImportMeta'"，导致无法正确识别Vite环境变量。

## 问题分析

这个问题是由于TypeScript编译器无法识别Vite特有的环境变量注入机制造成的。在Vite项目中，`import.meta.env`是一个特殊的对象，包含了所有以`VITE_`开头的环境变量。这些变量在运行时由Vite注入，但默认情况下TypeScript不知道这些类型定义。

错误发生在uiStore.ts文件中:

```typescript
if (import.meta.env.DEV && screenId === 'home') {
  const mockConfig = this.getMockScreenConfig(screenId);
  this.screens[screenId] = mockConfig;
  return mockConfig;
}
```

此外，在api.ts文件中存在额外的局部类型定义：

```typescript
// Vite环境变量类型声明
interface ImportMetaEnv {
  VITE_API_URL?: string;
  // 添加其他环境变量
}

// 为import.meta添加env类型
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

这导致了类型冲突，因为这些局部类型定义与全局类型定义发生冲突。

## 解决思路

解决此问题需要在项目中正确定义Vite环境变量的类型。Vite提供了内置的类型定义，可以通过在项目中添加或更新`vite-env.d.ts`文件来解决这个问题。我们需要确保：

1. 引用`vite/client`类型
2. 扩展`ImportMetaEnv`接口以添加项目特定的环境变量
3. 删除任何局部的`ImportMeta`接口定义
4. 添加适当的`tsconfig.json`配置

## 执行步骤

1. 创建或更新项目根目录下的`vite-env.d.ts`文件：

```typescript
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_PORT: string;
  readonly VITE_HOST: string;
  // more env variables...
  [key: string]: string | boolean | undefined;
}
```

2. 删除api.ts文件中的局部类型定义：
```typescript
// 删除以下代码
// Vite环境变量类型声明
interface ImportMetaEnv {
  VITE_API_URL?: string;
  // 添加其他环境变量
}

// 为import.meta添加env类型
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
```

3. 确保项目有正确的`tsconfig.json`配置：
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "lib": ["ESNext", "DOM"],
    "skipLibCheck": true,
    "noEmit": true,
    "types": ["vite/client"],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

4. 添加`tsconfig.node.json`配置文件：
```json
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Node",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

5. 添加Vue类型声明文件：
```typescript
// src/vue-shim.d.ts
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

6. 修复API函数中的any类型：
```typescript
// 修改前
getScreenConfig: async (screenId, context = {}) => {
// 修改后
getScreenConfig: async (screenId: string, context: Record<string, any> = {}) => {

// 修改前
getComponents: async (templateId) => {
// 修改后
getComponents: async (templateId: string) => {
```

## 结果验证

通过运行TypeScript编译器检查来验证错误是否已修复：

```bash
npx tsc --noEmit
```

执行后没有报错，表明所有TypeScript类型错误已经解决。

## 相关资源

- [Vite环境变量和模式文档](https://vitejs.dev/guide/env-and-mode.html)
- [TypeScript配置文档](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
- [Vue 3 + TypeScript + Vite最佳实践](https://vuejs.org/guide/typescript/overview.html)

## 注意事项

- 对于新增的环境变量，务必在`vite-env.d.ts`文件中添加相应的类型定义
- 避免在局部文件中定义`ImportMeta`或`ImportMetaEnv`接口，以防止类型冲突
- 如果项目结构变化，可能需要调整`tsconfig.json`中的`paths`和`include`配置 