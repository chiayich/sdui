<template>
  <div class="home">
    <SDUIRenderer :config="mockHomeConfig" />
  </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '../core/components/SDUIRenderer.vue';
import { mockHomeConfig } from '../services/mock/home-config';
</script>

<style scoped>
.home {
  min-height: 100vh;
}
</style> 