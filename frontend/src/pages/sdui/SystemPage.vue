<template>
  <div class="system-page">
    <SDUIRenderer :schema="'/api/v1/sdui/system'" />
  </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';
</script>

<style scoped>
.system-page {
  width: 100%;
}
</style>