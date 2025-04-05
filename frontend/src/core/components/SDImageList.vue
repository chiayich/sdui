<template>
  <div class="sd-image-list" :style="props.style">
    <div class="image-grid">
      <div 
        v-for="item in props.items" 
        :key="item.id" 
        class="image-item" 
        :class="{ 'selected': item.selected, 'highlight': item.highlight }"
      >
        <div class="image-placeholder">
          <i class="image-icon"></i>
        </div>
        <div class="image-id">{{ item.id }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ImageItem {
  id: string;
  selected?: boolean;
  highlight?: boolean;
}

interface Props {
  items: ImageItem[];
  style?: Record<string, string>;
}

const props = defineProps<Props>();
</script>

<style scoped>
.sd-image-list {
  width: 100%;
  margin-bottom: 16px;
}

.image-grid {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 4px;
  padding: 8px;
  background: #fff;
  border: 1px solid #f0f0f0;
  margin-bottom: 8px;
}

.image-item {
  flex: 0 0 auto;
  width: 80px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #e8e8e8;
  cursor: pointer;
  position: relative;
  transition: all 0.3s;
  border-radius: 2px;
  overflow: hidden;
}

.image-item.selected {
  border-color: rgb(24, 144, 255);
  background-color: rgba(24, 144, 255, 0.08);
}

.image-item.highlight::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 16px 16px 0;
  border-color: transparent #faad14 transparent transparent;
}

.image-placeholder {
  width: 70px;
  height: 70px;
  margin-top: 12px;
  background: #fafafa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-icon {
  width: 40px;
  height: 40px;
  background: #e0e0e0;
  border-radius: 2px;
}

.image-id {
  margin-top: 8px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
}
</style> 