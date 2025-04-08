<template>
  <header class="sd-header" :style="style">
    <slot>
      <component
        v-for="(child, index) in children"
        :key="index"
        :is="getComponentType(child.type)"
        v-bind="child.props || {}"
        :style="child.style"
      />
    </slot>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import componentMap from './index';

interface ComponentConfig {
  type: string;
  props?: Record<string, any>;
  style?: Record<string, any>;
  children?: ComponentConfig[];
}

const props = defineProps<{
  style?: Record<string, any>;
  children?: ComponentConfig[];
}>();

const getComponentType = (type: string) => {
  const componentType = componentMap[type.toLowerCase()];
  return componentType || 'div';
};
</script>

<style scoped>
.sd-header {
  width: 100%;
  padding: 1rem;
  background-color: var(--header-bg-color, #ffffff);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style> 