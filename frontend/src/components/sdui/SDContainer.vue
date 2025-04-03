<template>
  <div :id="id" class="sdui-container" :style="styleObj">
    <component
      v-for="child in children"
      :key="child.id"
      :is="getComponentType(child.type)"
      v-bind="mapProps(child)"
      @action="handleAction"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import componentMap from './index';
import { UIComponent, UIStyle, ComponentActionEvent } from '../../types/sdui';

// 定义组件属性
const props = defineProps<{
  id: string;
  style?: UIStyle;
  children?: UIComponent[];
}>();

// 定义事件
const emit = defineEmits<{
  (e: 'action', action: ComponentActionEvent): void;
}>();

// 将style对象转换为CSS对象
const styleObj = computed(() => props.style || {});

// 获取组件类型
const getComponentType = (type: string) => {
  return componentMap[type] || 'div';
};

// 映射组件属性
const mapProps = (component: UIComponent) => {
  return {
    id: component.id,
    style: component.style || {},
    properties: component.properties || {},
    events: component.events || {},
    children: component.children || [],
  };
};

// 处理子组件触发的事件
const handleAction = (action: ComponentActionEvent) => {
  emit('action', action);
};
</script>

<style scoped>
.sdui-container {
  display: flex;
  flex-direction: column;
}
</style> 