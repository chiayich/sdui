<template>
  <div class="organization-page">
    <SDUIRenderer :schema="'/api/sdui/system.organization'" />
  </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';
</script>

<style scoped>
.organization-page {
  width: 100%;
}
</style>