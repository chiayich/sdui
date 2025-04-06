<template>
    <div class="user-page">
        <SDUIRenderer :schema="'/api/v1/sdui/system.user'" />
    </div>
</template>

<script setup lang="ts">
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';
</script>

<style scoped>
.user-page {
    width: 100%;
}
</style>