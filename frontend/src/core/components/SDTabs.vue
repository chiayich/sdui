<template>
  <div class="sd-tabs">
    <div class="tabs-nav">
      <div
        v-for="item in props.items"
        :key="item.key"
        class="tab-item"
        :class="{ active: item.active }"
        @click="handleTabClick(item)"
      >
        {{ item.label }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface TabItem {
  key: string;
  label: string;
  active?: boolean;
}

interface Props {
  items: TabItem[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'update:active', key: string): void;
}>();

const handleTabClick = (item: TabItem) => {
  emit('update:active', item.key);
};
</script>

<style scoped>
.sd-tabs {
  margin-bottom: 16px;
}

.tabs-nav {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
  background: #fff;
  margin-bottom: 16px;
  user-select: none;
  position: relative;
}

.tab-item {
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.3s;
  margin-right: 32px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  line-height: 1.5715;
  position: relative;
}

.tab-item:hover {
  color: #40a9ff;
}

.tab-item.active {
  color: #1890ff;
  font-weight: 500;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #1890ff;
}
</style> 