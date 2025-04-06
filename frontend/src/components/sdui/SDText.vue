<template>
  <component :is="tagName" :id="id" :class="className" :style="finalStyle">
    {{ displayContent }}
    <slot></slot>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  content: {
    type: String,
    default: ''
  },
  level: {
    type: [String, Number],
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
  visible: {
    type: Boolean,
    default: true
  },
  properties: {
    type: Object,
    default: () => ({})
  }
});

const displayContent = computed(() => {
  return props.properties?.content || props.content || '';
});

const tagName = computed(() => {
  const level = props.properties?.level || props.level;

  if (level && /^[1-6]$/.test(String(level))) {
    return `h${level}`;
  }

  return 'p';
});

const finalStyle = computed(() => {
  const baseStyle = { ...(props.style || {}) };

  if (!props.visible) {
    baseStyle.display = 'none';
  }

  return baseStyle;
});
</script>

<style scoped>
h1,
h2,
h3,
h4,
h5,
h6,
p {
  margin: 0;
}
</style>