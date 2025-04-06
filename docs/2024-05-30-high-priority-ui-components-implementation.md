# SDUI高优先级组件实现

**日期**: 2024-05-30
**类别**: 前端
**紧急程度**: 高

## 问题描述

SDUI框架需要实现一系列高优先级组件，以覆盖核心业务场景。这些组件包括表单组件（输入框、选择器、复选框、单选框、开关）和布局组件（栅格布局、卡片、分割线）。这些组件是构建业务界面的基础元素，需要优先实现。

## 问题分析

在SDUI架构中，组件是前端渲染的基本单位，高优先级组件应当满足以下特性：

1. **通用性**：能够适应各种业务场景
2. **可配置性**：支持丰富的属性和样式配置
3. **事件支持**：提供完整的事件触发机制
4. **一致性**：与现有组件保持统一的API和样式风格
5. **响应式**：支持不同设备和屏幕尺寸

项目中已经实现了基础的容器、文本、按钮和输入框组件，但缺少更多的表单组件和布局组件。

## 解决思路

1. **组件划分**：将待实现组件分为表单组件和布局组件两大类
2. **接口统一**：所有组件保持一致的属性接口，包括id、properties、style、events等
3. **事件处理**：统一事件触发机制，通过emit('event')向上传递组件事件
4. **样式设计**：使用CSS变量实现主题定制，同时保持组件样式的一致性
5. **响应式支持**：布局组件特别关注响应式支持，栅格系统支持多种断点

## 执行步骤

### 1. 表单组件实现

#### 选择器组件 (SDSelect)
```vue
<template>
  <div class="sd-select" :style="style">
    <label v-if="properties.label" class="sd-select-label">
      {{ properties.label }}
      <span v-if="properties.required" class="required-mark">*</span>
    </label>
    <div class="select-wrapper" :class="{ 'is-error': hasError, 'is-disabled': properties.disabled }">
      <select
        :id="id"
        v-model="selectedValue"
        :name="properties.name"
        :disabled="properties.disabled"
        :multiple="properties.multiple"
        :placeholder="properties.placeholder"
        @change="handleChange"
      >
        <option v-if="properties.placeholder && !properties.multiple" value="" disabled>
          {{ properties.placeholder }}
        </option>
        <option
          v-for="option in properties.options"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
    </div>
  </div>
</template>
```

#### 复选框组件 (SDCheckbox)
```vue
<template>
  <div class="sd-checkbox" :style="style">
    <div class="checkbox-wrapper" :class="{ 'is-disabled': properties.disabled }">
      <label class="checkbox-label">
        <input
          type="checkbox"
          :id="id"
          :name="properties.name"
          :checked="isChecked"
          :disabled="properties.disabled"
          @change="handleChange"
        />
        <span class="checkbox-custom"></span>
        <span class="checkbox-text">
          {{ properties.label }}
        </span>
      </label>
    </div>
  </div>
</template>
```

#### 单选框组件 (SDRadio)
```vue
<template>
  <div class="sd-radio" :style="style">
    <div class="radio-group" :class="{ 'is-vertical': properties.vertical }">
      <div
        v-for="option in properties.options"
        :key="option.value"
        class="radio-wrapper"
      >
        <label class="radio-label">
          <input
            type="radio"
            :name="properties.name || id"
            :value="option.value"
            :checked="selectedValue === option.value"
            @change="handleChange(option.value)"
          />
          <span class="radio-custom"></span>
          <span class="radio-text">{{ option.label }}</span>
        </label>
      </div>
    </div>
  </div>
</template>
```

#### 开关组件 (SDSwitch)
```vue
<template>
  <div class="sd-switch" :style="style">
    <div class="switch-container">
      <span v-if="properties.labelPosition === 'left'" class="switch-label">
        {{ properties.label }}
      </span>
      
      <button
        :id="id"
        type="button"
        role="switch"
        class="switch"
        :class="{ 'is-checked': isChecked }"
        @click="toggle"
      >
        <span class="switch-core">
          <span class="switch-thumb"></span>
        </span>
      </button>
      
      <span v-if="properties.labelPosition !== 'left'" class="switch-label">
        {{ properties.label }}
      </span>
    </div>
  </div>
</template>
```

### 2. 布局组件实现

#### 栅格行组件 (SDRow)
```vue
<template>
  <div
    class="sd-row"
    :style="[
      style,
      {
        '--sd-row-gutter': properties.gutter ? `${properties.gutter}px` : '0px',
        '--sd-row-justify': properties.justify || 'flex-start',
        '--sd-row-align': properties.align || 'flex-start'
      }
    ]"
  >
    <slot></slot>
  </div>
</template>
```

#### 栅格列组件 (SDCol)
```vue
<template>
  <div
    class="sd-col"
    :style="[
      style,
      {
        '--sd-col-span': properties.span || 24,
        '--sd-col-offset': properties.offset || 0,
      }
    ]"
    :class="[
      properties.xs ? `sd-col-xs-${properties.xs}` : '',
      properties.sm ? `sd-col-sm-${properties.sm}` : '',
      properties.md ? `sd-col-md-${properties.md}` : '',
      properties.lg ? `sd-col-lg-${properties.lg}` : '',
      properties.xl ? `sd-col-xl-${properties.xl}` : ''
    ]"
  >
    <slot></slot>
  </div>
</template>
```

#### 卡片组件 (SDCard)
```vue
<template>
  <div
    class="sd-card"
    :class="{
      'is-hoverable': properties.hoverable,
      'is-bordered': properties.bordered,
      [`sd-card-${properties.size}`]: properties.size
    }"
    :style="style"
  >
    <div v-if="properties.title || properties.extra" class="sd-card-head">
      <div v-if="properties.title" class="sd-card-title">{{ properties.title }}</div>
      <div v-if="properties.extra" class="sd-card-extra">{{ properties.extra }}</div>
    </div>
    <div class="sd-card-body">
      <slot></slot>
    </div>
    <div v-if="properties.footer" class="sd-card-footer">
      {{ properties.footer }}
    </div>
  </div>
</template>
```

#### 分割线组件 (SDDivider)
```vue
<template>
  <div 
    class="sd-divider" 
    :class="{
      'sd-divider-vertical': properties.vertical,
      'sd-divider-dashed': properties.dashed,
      [`sd-divider-${properties.orientation}`]: properties.text && properties.orientation
    }"
    :style="style"
  >
    <span v-if="properties.text && !properties.vertical" class="sd-divider-inner-text">
      {{ properties.text }}
    </span>
  </div>
</template>
```

### 3. 组件注册

在组件映射表中注册所有新组件：

```typescript
// 导出组件映射表
const componentMap: ComponentMap = {
  container: SDContainer,
  text: SDText,
  button: SDButton,
  input: SDInput,
  list: SDList,
  table: SDTable,
  infiniteScroll: SDInfiniteScroll,
  select: SDSelect,
  checkbox: SDCheckbox,
  radio: SDRadio,
  switch: SDSwitch,
  row: SDRow,
  col: SDCol,
  card: SDCard,
  divider: SDDivider,
};
```

## 结果验证

所有组件都已成功实现，并在组件映射表中注册。组件遵循统一的接口和事件机制，可以在SDUI配置中使用。每个组件都支持以下功能：

1. **属性配置**：通过properties属性配置组件行为
2. **样式自定义**：通过style属性自定义组件样式
3. **事件处理**：通过events属性定义事件响应
4. **状态管理**：内部维护组件状态，并响应外部状态变化

## 相关资源

- [Vue 3文档](https://v3.vuejs.org/)
- [CSS变量指南](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)
- [栅格系统设计](https://ant.design/components/grid/)

## 注意事项

1. 所有组件都应使用CSS变量进行样式定义，以支持全局主题配置
2. 事件处理应遵循统一的事件触发机制
3. 组件属性应有合理的默认值，避免运行时错误
4. 响应式设计应考虑各种设备和屏幕尺寸 