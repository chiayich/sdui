<template>
  <div
    class="sd-col"
    :style="[
      style,
      {
        '--sd-col-span': properties.span || 24,
        '--sd-col-offset': properties.offset || 0,
        '--sd-col-padding': properties.gutter ? `0 calc(${properties.gutter}px / 2)` : '0'
      }
    ]"
    :class="[
      properties.xs ? `sd-col-xs-${properties.xs}` : '',
      properties.sm ? `sd-col-sm-${properties.sm}` : '',
      properties.md ? `sd-col-md-${properties.md}` : '',
      properties.lg ? `sd-col-lg-${properties.lg}` : '',
      properties.xl ? `sd-col-xl-${properties.xl}` : ''
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
      span: 24,       // 栅格占位格数，1-24
      offset: 0,      // 栅格左侧的间隔格数
      gutter: 0,      // 栅格间隔，从Row组件传递下来
      xs: undefined,  // <576px 响应式栅格
      sm: undefined,  // ≥576px 响应式栅格
      md: undefined,  // ≥768px 响应式栅格
      lg: undefined,  // ≥992px 响应式栅格
      xl: undefined   // ≥1200px 响应式栅格
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
.sd-col {
  position: relative;
  max-width: 100%;
  min-height: 1px;
  padding: var(--sd-col-padding);
  flex: 0 0 calc((var(--sd-col-span) / 24) * 100%);
  width: calc((var(--sd-col-span) / 24) * 100%);
  margin-left: calc((var(--sd-col-offset) / 24) * 100%);
}

/* 响应式栅格 */
@media screen and (max-width: 575px) {
  .sd-col-xs-1 { flex: 0 0 4.16667%; width: 4.16667%; }
  .sd-col-xs-2 { flex: 0 0 8.33333%; width: 8.33333%; }
  .sd-col-xs-3 { flex: 0 0 12.5%; width: 12.5%; }
  .sd-col-xs-4 { flex: 0 0 16.66667%; width: 16.66667%; }
  .sd-col-xs-5 { flex: 0 0 20.83333%; width: 20.83333%; }
  .sd-col-xs-6 { flex: 0 0 25%; width: 25%; }
  .sd-col-xs-7 { flex: 0 0 29.16667%; width: 29.16667%; }
  .sd-col-xs-8 { flex: 0 0 33.33333%; width: 33.33333%; }
  .sd-col-xs-9 { flex: 0 0 37.5%; width: 37.5%; }
  .sd-col-xs-10 { flex: 0 0 41.66667%; width: 41.66667%; }
  .sd-col-xs-11 { flex: 0 0 45.83333%; width: 45.83333%; }
  .sd-col-xs-12 { flex: 0 0 50%; width: 50%; }
  .sd-col-xs-13 { flex: 0 0 54.16667%; width: 54.16667%; }
  .sd-col-xs-14 { flex: 0 0 58.33333%; width: 58.33333%; }
  .sd-col-xs-15 { flex: 0 0 62.5%; width: 62.5%; }
  .sd-col-xs-16 { flex: 0 0 66.66667%; width: 66.66667%; }
  .sd-col-xs-17 { flex: 0 0 70.83333%; width: 70.83333%; }
  .sd-col-xs-18 { flex: 0 0 75%; width: 75%; }
  .sd-col-xs-19 { flex: 0 0 79.16667%; width: 79.16667%; }
  .sd-col-xs-20 { flex: 0 0 83.33333%; width: 83.33333%; }
  .sd-col-xs-21 { flex: 0 0 87.5%; width: 87.5%; }
  .sd-col-xs-22 { flex: 0 0 91.66667%; width: 91.66667%; }
  .sd-col-xs-23 { flex: 0 0 95.83333%; width: 95.83333%; }
  .sd-col-xs-24 { flex: 0 0 100%; width: 100%; }
}

@media screen and (min-width: 576px) {
  .sd-col-sm-1 { flex: 0 0 4.16667%; width: 4.16667%; }
  .sd-col-sm-2 { flex: 0 0 8.33333%; width: 8.33333%; }
  .sd-col-sm-3 { flex: 0 0 12.5%; width: 12.5%; }
  .sd-col-sm-4 { flex: 0 0 16.66667%; width: 16.66667%; }
  .sd-col-sm-5 { flex: 0 0 20.83333%; width: 20.83333%; }
  .sd-col-sm-6 { flex: 0 0 25%; width: 25%; }
  .sd-col-sm-7 { flex: 0 0 29.16667%; width: 29.16667%; }
  .sd-col-sm-8 { flex: 0 0 33.33333%; width: 33.33333%; }
  .sd-col-sm-9 { flex: 0 0 37.5%; width: 37.5%; }
  .sd-col-sm-10 { flex: 0 0 41.66667%; width: 41.66667%; }
  .sd-col-sm-11 { flex: 0 0 45.83333%; width: 45.83333%; }
  .sd-col-sm-12 { flex: 0 0 50%; width: 50%; }
  .sd-col-sm-13 { flex: 0 0 54.16667%; width: 54.16667%; }
  .sd-col-sm-14 { flex: 0 0 58.33333%; width: 58.33333%; }
  .sd-col-sm-15 { flex: 0 0 62.5%; width: 62.5%; }
  .sd-col-sm-16 { flex: 0 0 66.66667%; width: 66.66667%; }
  .sd-col-sm-17 { flex: 0 0 70.83333%; width: 70.83333%; }
  .sd-col-sm-18 { flex: 0 0 75%; width: 75%; }
  .sd-col-sm-19 { flex: 0 0 79.16667%; width: 79.16667%; }
  .sd-col-sm-20 { flex: 0 0 83.33333%; width: 83.33333%; }
  .sd-col-sm-21 { flex: 0 0 87.5%; width: 87.5%; }
  .sd-col-sm-22 { flex: 0 0 91.66667%; width: 91.66667%; }
  .sd-col-sm-23 { flex: 0 0 95.83333%; width: 95.83333%; }
  .sd-col-sm-24 { flex: 0 0 100%; width: 100%; }
}

@media screen and (min-width: 768px) {
  .sd-col-md-1 { flex: 0 0 4.16667%; width: 4.16667%; }
  .sd-col-md-2 { flex: 0 0 8.33333%; width: 8.33333%; }
  .sd-col-md-3 { flex: 0 0 12.5%; width: 12.5%; }
  .sd-col-md-4 { flex: 0 0 16.66667%; width: 16.66667%; }
  .sd-col-md-5 { flex: 0 0 20.83333%; width: 20.83333%; }
  .sd-col-md-6 { flex: 0 0 25%; width: 25%; }
  .sd-col-md-7 { flex: 0 0 29.16667%; width: 29.16667%; }
  .sd-col-md-8 { flex: 0 0 33.33333%; width: 33.33333%; }
  .sd-col-md-9 { flex: 0 0 37.5%; width: 37.5%; }
  .sd-col-md-10 { flex: 0 0 41.66667%; width: 41.66667%; }
  .sd-col-md-11 { flex: 0 0 45.83333%; width: 45.83333%; }
  .sd-col-md-12 { flex: 0 0 50%; width: 50%; }
  .sd-col-md-13 { flex: 0 0 54.16667%; width: 54.16667%; }
  .sd-col-md-14 { flex: 0 0 58.33333%; width: 58.33333%; }
  .sd-col-md-15 { flex: 0 0 62.5%; width: 62.5%; }
  .sd-col-md-16 { flex: 0 0 66.66667%; width: 66.66667%; }
  .sd-col-md-17 { flex: 0 0 70.83333%; width: 70.83333%; }
  .sd-col-md-18 { flex: 0 0 75%; width: 75%; }
  .sd-col-md-19 { flex: 0 0 79.16667%; width: 79.16667%; }
  .sd-col-md-20 { flex: 0 0 83.33333%; width: 83.33333%; }
  .sd-col-md-21 { flex: 0 0 87.5%; width: 87.5%; }
  .sd-col-md-22 { flex: 0 0 91.66667%; width: 91.66667%; }
  .sd-col-md-23 { flex: 0 0 95.83333%; width: 95.83333%; }
  .sd-col-md-24 { flex: 0 0 100%; width: 100%; }
}

@media screen and (min-width: 992px) {
  .sd-col-lg-1 { flex: 0 0 4.16667%; width: 4.16667%; }
  .sd-col-lg-2 { flex: 0 0 8.33333%; width: 8.33333%; }
  .sd-col-lg-3 { flex: 0 0 12.5%; width: 12.5%; }
  .sd-col-lg-4 { flex: 0 0 16.66667%; width: 16.66667%; }
  .sd-col-lg-5 { flex: 0 0 20.83333%; width: 20.83333%; }
  .sd-col-lg-6 { flex: 0 0 25%; width: 25%; }
  .sd-col-lg-7 { flex: 0 0 29.16667%; width: 29.16667%; }
  .sd-col-lg-8 { flex: 0 0 33.33333%; width: 33.33333%; }
  .sd-col-lg-9 { flex: 0 0 37.5%; width: 37.5%; }
  .sd-col-lg-10 { flex: 0 0 41.66667%; width: 41.66667%; }
  .sd-col-lg-11 { flex: 0 0 45.83333%; width: 45.83333%; }
  .sd-col-lg-12 { flex: 0 0 50%; width: 50%; }
  .sd-col-lg-13 { flex: 0 0 54.16667%; width: 54.16667%; }
  .sd-col-lg-14 { flex: 0 0 58.33333%; width: 58.33333%; }
  .sd-col-lg-15 { flex: 0 0 62.5%; width: 62.5%; }
  .sd-col-lg-16 { flex: 0 0 66.66667%; width: 66.66667%; }
  .sd-col-lg-17 { flex: 0 0 70.83333%; width: 70.83333%; }
  .sd-col-lg-18 { flex: 0 0 75%; width: 75%; }
  .sd-col-lg-19 { flex: 0 0 79.16667%; width: 79.16667%; }
  .sd-col-lg-20 { flex: 0 0 83.33333%; width: 83.33333%; }
  .sd-col-lg-21 { flex: 0 0 87.5%; width: 87.5%; }
  .sd-col-lg-22 { flex: 0 0 91.66667%; width: 91.66667%; }
  .sd-col-lg-23 { flex: 0 0 95.83333%; width: 95.83333%; }
  .sd-col-lg-24 { flex: 0 0 100%; width: 100%; }
}

@media screen and (min-width: 1200px) {
  .sd-col-xl-1 { flex: 0 0 4.16667%; width: 4.16667%; }
  .sd-col-xl-2 { flex: 0 0 8.33333%; width: 8.33333%; }
  .sd-col-xl-3 { flex: 0 0 12.5%; width: 12.5%; }
  .sd-col-xl-4 { flex: 0 0 16.66667%; width: 16.66667%; }
  .sd-col-xl-5 { flex: 0 0 20.83333%; width: 20.83333%; }
  .sd-col-xl-6 { flex: 0 0 25%; width: 25%; }
  .sd-col-xl-7 { flex: 0 0 29.16667%; width: 29.16667%; }
  .sd-col-xl-8 { flex: 0 0 33.33333%; width: 33.33333%; }
  .sd-col-xl-9 { flex: 0 0 37.5%; width: 37.5%; }
  .sd-col-xl-10 { flex: 0 0 41.66667%; width: 41.66667%; }
  .sd-col-xl-11 { flex: 0 0 45.83333%; width: 45.83333%; }
  .sd-col-xl-12 { flex: 0 0 50%; width: 50%; }
  .sd-col-xl-13 { flex: 0 0 54.16667%; width: 54.16667%; }
  .sd-col-xl-14 { flex: 0 0 58.33333%; width: 58.33333%; }
  .sd-col-xl-15 { flex: 0 0 62.5%; width: 62.5%; }
  .sd-col-xl-16 { flex: 0 0 66.66667%; width: 66.66667%; }
  .sd-col-xl-17 { flex: 0 0 70.83333%; width: 70.83333%; }
  .sd-col-xl-18 { flex: 0 0 75%; width: 75%; }
  .sd-col-xl-19 { flex: 0 0 79.16667%; width: 79.16667%; }
  .sd-col-xl-20 { flex: 0 0 83.33333%; width: 83.33333%; }
  .sd-col-xl-21 { flex: 0 0 87.5%; width: 87.5%; }
  .sd-col-xl-22 { flex: 0 0 91.66667%; width: 91.66667%; }
  .sd-col-xl-23 { flex: 0 0 95.83333%; width: 95.83333%; }
  .sd-col-xl-24 { flex: 0 0 100%; width: 100%; }
}
</style> 