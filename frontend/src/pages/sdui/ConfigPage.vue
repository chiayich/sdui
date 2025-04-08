<template>
    <div class="config-page">
        <SDUIRenderer :schema="'/api/sdui/system.config'" />
    </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';
</script>

<style scoped>
.config-page {
    width: 100%;
}
</style>