# SDUI 前端组件增强计划

**日期**: 2024-04-05  
**作者**: 前端团队  
**状态**: 草稿

## 概述

本文档详细说明SDUI项目前端组件库的扩展计划，包括组件类型、属性标准、实现优先级和测试策略。该计划旨在完善前端渲染引擎，提供更丰富的UI表现力。

## 当前状态

目前已实现的基础组件:
- 容器组件 (SDContainer)
- 文本组件 (SDText)
- 按钮组件 (SDButton)

## 组件扩展计划

### 1. 表单组件 (优先级: 高)

**计划周期**: 2天

#### 1.1 输入框组件 (SDInput)

```vue
<template>
  <div class="sd-input" :style="style">
    <label v-if="properties.label" :for="id">{{ properties.label }}</label>
    <input
      :id="id"
      :type="properties.type || 'text'"
      :value="modelValue"
      @input="updateValue"
      :placeholder="properties.placeholder"
      :disabled="properties.disabled"
      :readonly="properties.readonly"
    />
    <small v-if="properties.helpText" class="help-text">{{ properties.helpText }}</small>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps({
  id: String,
  properties: {
    type: Object,
    default: () => ({})
  },
  style: {
    type: Object,
    default: () => ({})
  },
  modelValue: [String, Number]
});

const emit = defineEmits(['update:modelValue', 'action']);

const updateValue = (event) => {
  const value = event.target.value;
  emit('update:modelValue', value);
  
  if (props.properties.onChange) {
    emit('action', {
      type: 'input',
      componentId: props.id,
      value,
      event: props.properties.onChange
    });
  }
};
</script>

<style scoped>
.sd-input {
  margin-bottom: 16px;
}

.sd-input label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.sd-input input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: border-color 0.2s;
}

.sd-input input:focus {
  outline: none;
  border-color: #409eff;
}

.sd-input .help-text {
  display: block;
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
}
</style>
```

#### 1.2 选择器组件 (SDSelect)

```vue
<template>
  <div class="sd-select" :style="style">
    <label v-if="properties.label" :for="id">{{ properties.label }}</label>
    <select
      :id="id"
      :value="modelValue"
      @change="updateValue"
      :disabled="properties.disabled"
    >
      <option v-if="properties.placeholder" value="" disabled selected>
        {{ properties.placeholder }}
      </option>
      <option
        v-for="option in properties.options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
    <small v-if="properties.helpText" class="help-text">{{ properties.helpText }}</small>
  </div>
</template>

<script setup lang="ts">
// 类似SDInput的实现
</script>
```

#### 1.3 复选框组件 (SDCheckbox)
#### 1.4 单选框组件 (SDRadio)
#### 1.5 开关组件 (SDSwitch)

### 2. 布局组件 (优先级: 高)

**计划周期**: 1天

#### 2.1 栅格行组件 (SDRow)
#### 2.2 栅格列组件 (SDCol)
#### 2.3 卡片组件 (SDCard)
#### 2.4 分割线组件 (SDDivider)

### 3. 数据展示组件 (优先级: 中)

**计划周期**: 2天

#### 3.1 表格组件 (SDTable)
```vue
<template>
  <div class="sd-table" :style="style">
    <table>
      <thead>
        <tr>
          <th v-for="column in properties.columns" :key="column.key">
            {{ column.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in properties.data" :key="rowIndex">
          <td v-for="column in properties.columns" :key="column.key">
            {{ row[column.key] }}
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="properties.pagination" class="sd-table-pagination">
      <!-- 分页控件 -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  id: String,
  properties: {
    type: Object,
    default: () => ({})
  },
  style: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['action']);

const handleRowClick = (row, index) => {
  if (props.properties.onRowClick) {
    emit('action', {
      type: 'row_click',
      componentId: props.id,
      row,
      index,
      event: props.properties.onRowClick
    });
  }
};
</script>
```

#### 3.2 列表组件 (SDList)
#### 3.3 标签组件 (SDTag)
#### 3.4 进度条组件 (SDProgress)

### 4. 导航组件 (优先级: 中)

**计划周期**: 1天

#### 4.1 标签页组件 (SDTabs)
#### 4.2 菜单组件 (SDMenu)
#### 4.3 分页组件 (SDPagination)
#### 4.4 步骤条组件 (SDSteps)

### 5. 反馈组件 (优先级: 低)

**计划周期**: 1天

#### 5.1 对话框组件 (SDDialog)
#### 5.2 消息提示组件 (SDMessage)
#### 5.3 加载中组件 (SDLoading)
#### 5.4 警告提示组件 (SDAlert)

## 组件属性标准

为了保持一致性，所有组件应遵循以下属性标准:

```typescript
// 基础组件接口
interface SDUIComponent {
  // 组件必需属性
  id: string;                   // 组件唯一标识
  type: string;                 // 组件类型
  
  // 可选通用属性
  properties?: Record<string, any>; // 组件属性
  style?: Record<string, any>;      // 样式属性
  events?: Record<string, any>;     // 事件处理
  children?: SDUIComponent[];       // 子组件
  
  // 高级属性（可选）
  visible?: boolean;            // 是否可见
  disabled?: boolean;           // 是否禁用
  data?: any;                   // 组件数据
  bindings?: Record<string, any>; // 数据绑定
}
```

### 通用组件属性

每种组件类型都应支持以下通用属性:

1. **基础属性**
   - `id`: 组件唯一标识
   - `type`: 组件类型
   - `visible`: 是否可见
   - `disabled`: 是否禁用

2. **样式属性**
   - `style`: 内联样式对象
   - `className`: 自定义CSS类名

3. **事件属性**
   - `onClick`: 点击事件
   - `onMouseEnter`: 鼠标进入事件
   - `onMouseLeave`: 鼠标离开事件

## 组件注册机制

组件注册采用集中管理的方式，通过 `index.ts` 统一导出:

```typescript
// frontend/src/components/sdui/index.ts
import { Component } from 'vue';
import SDContainer from './SDContainer.vue';
import SDText from './SDText.vue';
import SDButton from './SDButton.vue';
import SDInput from './SDInput.vue';
import SDSelect from './SDSelect.vue';
// ... 导入其他组件

// 定义组件映射表接口
interface ComponentMap {
  [key: string]: Component;
}

// 导出组件映射表
const componentMap: ComponentMap = {
  container: SDContainer,
  text: SDText,
  button: SDButton,
  input: SDInput,
  select: SDSelect,
  // ... 其他组件映射
};

export default componentMap;
```

## 组件测试计划

为保证组件质量，将采用以下测试策略:

1. **单元测试**
   - 使用 Vitest 进行组件单元测试
   - 测试组件渲染、属性传递和事件处理

2. **交互测试**
   - 使用 Vue Test Utils 测试用户交互
   - 模拟点击、输入等用户操作

3. **快照测试**
   - 使用 Jest 快照测试确保UI一致性
   - 检测非预期的UI变化

4. **端到端测试**
   - 在实际渲染环境中验证组件
   - 测试组件与SDUI渲染器的集成

## 组件文档与示例

为每个组件创建文档和示例:

1. **组件文档**
   - 组件描述
   - 属性API表格
   - 事件列表
   - 使用示例

2. **组件示例**
   - 基本用法
   - 高级配置
   - 样式变体
   - 与其他组件交互

## 工作量估计

| 组件分类 | 组件数量 | 工作量（人天） |
|---------|---------|--------------|
| 表单组件 | 5       | 2            |
| 布局组件 | 4       | 1            |
| 数据展示 | 4       | 2            |
| 导航组件 | 4       | 1            |
| 反馈组件 | 4       | 1            |
| 测试和文档 | -     | 2            |
| **总计** | **21** | **9**        |

## 实施步骤

1. **准备工作** (0.5天)
   - 定义组件接口和属性标准
   - 创建组件测试框架
   - 设置文档生成工具

2. **组件开发** (6天)
   - 按优先级实现各类组件
   - 编写单元测试
   - 创建使用示例

3. **集成与测试** (1.5天)
   - 将组件集成到SDUI渲染器
   - 进行集成测试
   - 性能优化

4. **文档完善** (1天)
   - 编写组件文档
   - 创建示例页面
   - 整理设计规范

## 风险与挑战

1. **复杂组件实现**
   - 表格、树形控件等复杂组件可能需要更多时间
   - 缓解：可先实现基本功能，后续迭代增强

2. **样式一致性**
   - 确保所有组件遵循统一的设计风格
   - 缓解：创建共享样式变量和混入

3. **性能问题**
   - 大量使用动态组件可能导致性能下降
   - 缓解：实现组件懒加载，优化渲染性能

## 后续计划

1. **组件主题支持**
   - 实现亮色/暗色主题切换
   - 支持自定义主题变量

2. **组件国际化**
   - 支持多语言文本
   - 适配不同区域的日期、数字格式

3. **可访问性增强**
   - 增加ARIA属性支持
   - 改进键盘导航支持 