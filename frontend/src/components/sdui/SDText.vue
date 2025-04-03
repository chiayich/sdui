<template>
  <div :id="id" class="sdui-text" :style="styleObj">
    {{ content }}
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { UIStyle, UIProperties } from '../../types/sdui';

// 定义组件属性
const props = defineProps<{
  id: string;
  style?: UIStyle;
  properties?: UIProperties;
}>();

// 计算文本内容
const content = computed(() => {
  if (props.properties && 'content' in props.properties) {
    return props.properties.content;
  }
  return '';
});

// 将style对象转换为CSS对象
const styleObj = computed(() => props.style || {});
</script>

<style scoped>
.sdui-text {
  margin: 0;
}
</style> 