<template>
  <div 
    class="sd-divider" 
    :class="{
      'sd-divider-vertical': properties.vertical,
      'sd-divider-dashed': properties.dashed,
      [`sd-divider-${properties.orientation}`]: properties.text && properties.orientation
    }"
    :style="style"
  >
    <span v-if="properties.text && !properties.vertical" class="sd-divider-inner-text">
      {{ properties.text }}
    </span>
  </div>
</template>

<script setup lang="ts">
defineProps({
  id: {
    type: String,
    required: true
  },
  properties: {
    type: Object,
    required: true,
    default: () => ({
      vertical: false,       // 是否垂直分割线
      dashed: false,        // 是否虚线
      text: '',             // 分割线文本
      orientation: 'center' // 文本位置 left | center | right
    })
  },
  style: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  }
});
</script>

<style scoped>
.sd-divider {
  box-sizing: border-box;
  margin: 16px 0;
  padding: 0;
  color: var(--text-color, #333);
  font-size: 14px;
  font-variant: tabular-nums;
  line-height: 1.5;
  list-style: none;
  background: var(--divider-color, #f0f0f0);
  clear: both;
  width: 100%;
  min-width: 100%;
  height: 1px;
  position: relative;
}

.sd-divider-vertical {
  margin: 0 8px;
  display: inline-block;
  height: 0.9em;
  width: 1px;
  min-width: 1px;
  vertical-align: middle;
}

.sd-divider-dashed {
  background: none;
  border-top: 1px dashed var(--divider-color, #f0f0f0);
  height: 0;
}

.sd-divider-vertical.sd-divider-dashed {
  border-top: 0;
  border-left: 1px dashed var(--divider-color, #f0f0f0);
  height: 0.9em;
  width: 0;
}

.sd-divider-inner-text {
  display: inline-block;
  padding: 0 16px;
  font-weight: 500;
  font-size: 14px;
  color: var(--text-color, #333);
  background: var(--bg-color, #fff);
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

.sd-divider-center {
  display: flex;
  align-items: center;
  justify-content: center;
  height: auto;
  margin: 16px 0;
}

.sd-divider-center::before,
.sd-divider-center::after {
  content: '';
  display: block;
  flex: 1;
  height: 1px;
  background: var(--divider-color, #f0f0f0);
}

.sd-divider-center.sd-divider-dashed::before,
.sd-divider-center.sd-divider-dashed::after {
  border-top: 1px dashed var(--divider-color, #f0f0f0);
  background: none;
  height: 0;
}

.sd-divider-left::before {
  width: 5%;
}

.sd-divider-left::after {
  width: 95%;
}

.sd-divider-right::before {
  width: 95%;
}

.sd-divider-right::after {
  width: 5%;
}

.sd-divider-left .sd-divider-inner-text {
  left: 5%;
  transform: translateY(-50%) translateX(-50%);
}

.sd-divider-right .sd-divider-inner-text {
  right: 5%;
  transform: translateY(-50%) translateX(50%);
}
</style> 