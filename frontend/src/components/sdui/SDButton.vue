<template>
  <button
    :class="[
      'sd-button',
      `sd-button--${type}`,
      `sd-button--${size}`,
      { 'is-disabled': disabled }
    ]"
    :disabled="disabled"
    @click="handleClick"
  >
    <i v-if="icon" :class="icon" />
    <slot />
  </button>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

interface Props {
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info' | 'text';
  size?: 'large' | 'default' | 'small';
  icon?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'primary',
  size: 'default',
  icon: '',
  disabled: false,
});

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void;
}>();

const handleClick = (event: MouseEvent) => {
  if (props.disabled) return;
  emit('click', event);
};
</script>

<style lang="scss" scoped>
.sd-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid transparent;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  cursor: pointer;
  transition: all 0.3s;
  
  &--primary {
    background-color: var(--primary-color, #1890ff);
    color: #fff;
    
    &:hover {
      background-color: var(--primary-color-hover, #40a9ff);
    }
  }
  
  &--success {
    background-color: var(--success-color, #52c41a);
    color: #fff;
    
    &:hover {
      background-color: var(--success-color-hover, #73d13d);
    }
  }
  
  &--warning {
    background-color: var(--warning-color, #faad14);
    color: #fff;
    
    &:hover {
      background-color: var(--warning-color-hover, #ffc53d);
    }
  }
  
  &--danger {
    background-color: var(--danger-color, #ff4d4f);
    color: #fff;
    
    &:hover {
      background-color: var(--danger-color-hover, #ff7875);
    }
  }
  
  &--info {
    background-color: var(--info-color, #909399);
    color: #fff;
    
    &:hover {
      background-color: var(--info-color-hover, #a6a9ad);
    }
  }
  
  &--text {
    background-color: transparent;
    color: var(--primary-color, #1890ff);
    padding: 0;
    
    &:hover {
      color: var(--primary-color-hover, #40a9ff);
    }
  }
  
  &--large {
    padding: 12px 20px;
    font-size: 16px;
  }
  
  &--small {
    padding: 4px 12px;
    font-size: 12px;
  }
  
  &.is-disabled {
    cursor: not-allowed;
    opacity: 0.6;
    
    &:hover {
      opacity: 0.6;
    }
  }
  
  i {
    margin-right: 4px;
  }
}
</style> 