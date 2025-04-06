<template>
  <button :id="id" :class="['sd-button', `sd-button--${buttonType}`, className]" :style="finalStyle"
    @click="handleClick">
    {{ buttonText }}
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  text: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'default' // default, primary, success, warning, danger
  },
  className: {
    type: String,
    default: ''
  },
  style: {
    type: Object,
    default: () => ({})
  },
  visible: {
    type: Boolean,
    default: true
  },
  properties: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['action', 'click']);

// 计算按钮文本
const buttonText = computed(() => {
  // 兼容多种属性名: text, label
  return props.properties?.text || props.properties?.label || props.text || '';
});

// 计算按钮类型
const buttonType = computed(() => {
  return props.properties?.type || props.type || 'default';
});

// 计算最终样式
const finalStyle = computed(() => {
  const baseStyle = { ...(props.style || {}) };

  if (!props.visible) {
    baseStyle.display = 'none';
  }

  return baseStyle;
});

// 处理点击事件
const handleClick = (event: MouseEvent) => {
  // 发出基本点击事件
  emit('click', event);

  // 如果有定义事件处理器，根据配置发出action
  if (props.events?.click) {
    emit('action', props.events.click);
  } else if (props.properties?.action) {
    emit('action', props.properties.action);
  }
};
</script>

<style scoped>
.sd-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.sd-button--default {
  background-color: #f5f5f5;
  color: #333;
}

.sd-button--primary {
  background-color: #409eff;
  color: white;
}

.sd-button--success {
  background-color: #67c23a;
  color: white;
}

.sd-button--warning {
  background-color: #e6a23c;
  color: white;
}

.sd-button--danger {
  background-color: #f56c6c;
  color: white;
}

.sd-button:hover {
  opacity: 0.8;
}

.sd-button:active {
  transform: scale(0.98);
}
</style>