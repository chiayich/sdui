<template>
  <div class="sd-tags">
    <span v-if="label" class="tags-label">{{ label }}</span>
    <div class="tags-container">
      <div
        v-for="tag in tags"
        :key="tag.id"
        class="tag"
      >
        <span class="tag-text">{{ tag.text }}</span>
        <span v-if="tag.closable" class="tag-close" @click="handleClose(tag)">×</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Tag {
  id: string;
  text: string;
  closable?: boolean;
}

interface Props {
  label?: string;
  tags?: Tag[];
}

const props = defineProps<Props>();
const emit = defineEmits(['close']);

const handleClose = (tag: Tag) => {
  emit('close', tag);
};
</script>

<style scoped>
.sd-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.tags-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.85);
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 7px;
  font-size: 12px;
  line-height: 20px;
  white-space: nowrap;
  background-color: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  cursor: default;
  transition: all 0.3s;
}

.tag-text {
  color: rgba(0, 0, 0, 0.65);
}

.tag-close {
  margin-left: 4px;
  color: rgba(0, 0, 0, 0.45);
  cursor: pointer;
  font-size: 10px;
  font-weight: bold;
  transition: all 0.3s;
}

.tag-close:hover {
  color: rgba(0, 0, 0, 0.85);
}
</style> 