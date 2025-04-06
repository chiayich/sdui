<template>
  <div class="role-page">
    <SDUIRenderer :schema="'/api/v1/sdui/system.role'" />
  </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';
</script>

<style scoped>
.role-page {
  width: 100%;
}
</style>