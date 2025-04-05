<template>
  <div class="sd-date-range-picker" :style="style">
    <input 
      type="text" 
      class="date-input" 
      readonly
      :placeholder="placeholder || '选择日期'"
      :value="value"
    />
    <div class="date-icon">📅</div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  placeholder?: string;
  style?: Record<string, string>;
  value?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:value']);
</script>

<style scoped>
.sd-date-range-picker {
  position: relative;
  width: 100%;
  min-width: 120px;
}

.date-input {
  width: 100%;
  padding: 4px 30px 4px 11px;
  height: 32px;
  line-height: 1.5;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  cursor: pointer;
}

.date-icon {
  position: absolute;
  right: 11px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #666;
  pointer-events: none;
}
</style> 