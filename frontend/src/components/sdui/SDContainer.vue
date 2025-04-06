<template>
  <div :id="id" :class="['sd-container', className]" :style="finalStyle">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface SDUIChild {
  id?: string;
  component: string | object;
  props: Record<string, any>;
}

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  className: {
    type: String,
    default: ''
  },
  style: {
    type: Object,
    default: () => ({})
  },
  children: {
    type: Array as () => SDUIChild[],
    default: () => []
  },
  content: {
    type: Array as () => SDUIChild[],
    default: () => []
  },
  visible: {
    type: Boolean,
    default: true
  },
  properties: {
    type: Object,
    default: () => ({})
  }
});

const finalStyle = computed(() => {
  const baseStyle = { ...(props.style || {}) };

  if (props.properties && props.properties.style) {
    Object.assign(baseStyle, props.properties.style);
  }

  if (!props.visible) {
    baseStyle.display = 'none';
  }

  return baseStyle;
});

defineEmits(['action']);
</script>

<style scoped>
.sd-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  box-sizing: border-box;
}
</style>