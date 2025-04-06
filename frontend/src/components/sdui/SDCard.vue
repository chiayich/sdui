<template>
  <div class="sd-card" :class="{
    'is-hoverable': properties.hoverable,
    'is-bordered': properties.bordered,
    [`sd-card-${properties.size}`]: properties.size
  }" :style="style">
    <div v-if="properties.title || hasExtra" class="sd-card-head">
      <div v-if="properties.title" class="sd-card-title">{{ properties.title }}</div>
      <div v-if="hasExtra" class="sd-card-extra">
        <!-- 处理字符串类型的extra -->
        <template v-if="typeof properties.extra === 'string'">
          {{ properties.extra }}
        </template>

        <!-- 处理数组类型的extra，用于渲染按钮等组件 -->
        <template v-else-if="Array.isArray(properties.extra)">
          <component-renderer v-for="(item, index) in properties.extra" :key="`extra-${index}`" :component="item"
            :context="context" @action="handleAction" />
        </template>
      </div>
    </div>
    <div class="sd-card-body" :style="{ padding: properties.bodyPadding }">
      <slot></slot>
    </div>
    <div v-if="properties.footer" class="sd-card-footer">
      {{ properties.footer }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import ComponentRenderer from './ComponentRenderer.vue';

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  properties: {
    type: Object,
    required: true,
    default: () => ({
      title: '',     // 卡片标题
      extra: '',     // 卡片右上角的操作区域
      bordered: true, // 是否有边框
      hoverable: false, // 鼠标悬浮时是否有阴影效果
      bodyPadding: '16px', // 内容区域的内边距
      size: 'default', // 卡片大小 small | default | large
      footer: '' // 卡片底部内容
    })
  },
  style: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  },
  context: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['action']);

// 是否有额外操作区域
const hasExtra = computed(() => {
  return !!props.properties.extra;
});

// 处理组件动作
const handleAction = (action: any) => {
  emit('action', action);
};
</script>

<style scoped>
.sd-card {
  position: relative;
  background-color: var(--card-bg, #fff);
  border-radius: 4px;
  transition: all 0.3s;
  margin-bottom: 16px;
}

.sd-card.is-bordered {
  border: 1px solid var(--border-color, #ebedf0);
}

.sd-card.is-hoverable:hover {
  box-shadow: 0 1px 2px -2px rgba(0, 0, 0, 0.16),
    0 3px 6px 0 rgba(0, 0, 0, 0.12),
    0 5px 12px 4px rgba(0, 0, 0, 0.09);
}

.sd-card-small .sd-card-head {
  min-height: 36px;
  padding: 8px 12px;
}

.sd-card-small .sd-card-body {
  padding: 12px;
}

.sd-card-large .sd-card-head {
  min-height: 56px;
  padding: 16px 24px;
}

.sd-card-large .sd-card-body {
  padding: 24px;
}

.sd-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 48px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color, #ebedf0);
}

.sd-card-title {
  font-weight: 500;
  font-size: 16px;
  color: var(--text-color, #333);
}

.sd-card-extra {
  color: var(--text-light, #999);
}

.sd-card-body {
  padding: 16px;
}

.sd-card-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--border-color, #ebedf0);
  color: var(--text-light, #999);
}
</style>