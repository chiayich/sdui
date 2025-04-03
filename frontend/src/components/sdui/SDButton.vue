<template>
  <button 
    :id="id" 
    class="sdui-button" 
    :style="styleObj"
    @click="handleClick"
  >
    {{ label }}
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { UIStyle, UIProperties, UIEvents, ComponentActionEvent } from '../../types/sdui';

// 定义组件属性
const props = defineProps<{
  id: string;
  style?: UIStyle;
  properties?: UIProperties;
  events?: UIEvents;
}>();

// 定义事件
const emit = defineEmits<{
  (e: 'action', action: ComponentActionEvent): void;
}>();

// 计算按钮文本
const label = computed(() => {
  if (props.properties && 'label' in props.properties) {
    return props.properties.label;
  }
  return 'Button';
});

// 将style对象转换为CSS对象
const styleObj = computed(() => props.style || {});

// 处理点击事件
const handleClick = () => {
  // 如果定义了点击事件，则触发
  if (props.events && props.events.click) {
    const actionData = {
      componentId: props.id,
      ...props.events.click
    };
    emit('action', actionData);
  }
};
</script>

<style scoped>
.sdui-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  background-color: #1890ff;
  color: white;
}

.sdui-button:hover {
  opacity: 0.9;
}

.sdui-button:active {
  opacity: 0.7;
}
</style> 