<template>
  <div class="sdui-page">
    <SDUIRenderer :config="config" />
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';
import SDUIRenderer from '@/core/components/SDUIRenderer.vue';
import { PageConfig } from '@/core/types/page';

defineProps<{
  config: PageConfig;
}>();
</script>

<style scoped>
.sdui-page {
  width: 100%;
  height: 100%;
}
</style> 