<template>
  <span class="sd-text" :style="props.style">{{ props.content }}</span>
</template>

<script setup lang="ts">
interface Props {
  content: string;
  style?: Record<string, string>;
}

const props = defineProps<Props>();
</script>

<style scoped>
.sd-text {
  display: inline-block;
}
</style> 