<template>
  <div
    class="sd-row"
    :style="[
      style,
      {
        '--sd-row-gutter': properties.gutter ? `${properties.gutter}px` : '0px',
        '--sd-row-justify': properties.justify || 'flex-start',
        '--sd-row-align': properties.align || 'flex-start'
      }
    ]"
  >
    <slot></slot>
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
      gutter: 0,
      justify: 'flex-start', // 水平对齐: flex-start, flex-end, center, space-between, space-around
      align: 'flex-start',   // 垂直对齐: flex-start, flex-end, center, stretch
      wrap: true            // 是否换行
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
  children: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
.sd-row {
  display: flex;
  flex-wrap: v-bind('properties.wrap ? "wrap" : "nowrap"');
  margin: calc(var(--sd-row-gutter) / -2);
  justify-content: var(--sd-row-justify);
  align-items: var(--sd-row-align);
  width: calc(100% + var(--sd-row-gutter));
}
</style> 