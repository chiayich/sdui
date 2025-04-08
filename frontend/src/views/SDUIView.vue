<template>
  <div class="sdui-view">
    <SDUIRenderer :schema="actualSchema" @loaded="handleLoaded" @error="handleError" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import SDUIRenderer from '@/components/sdui/SDUIRenderer.vue';

const route = useRoute();
const router = useRouter();

// 组件属性
const props = defineProps({
  schema: {
    type: String,
    default: ''
  }
});

// 错误状态
const error = ref(null);

// 最终的API路径
const actualSchema = computed(() => {
  if (props.schema) {
    return props.schema;
  }

  // 从路由参数中获取screenId
  if (route.params.screenId) {
    // 返回完整的API路径
    return `/api/sdui/${route.params.screenId}`;
  }

  return '';
});

// 用于存储额外的配置数据
const configData = ref(null);

// 挂载时检查路由参数
onMounted(() => {
  // 如果没有指定schema且没有screenId参数，跳转到首页
  if (actualSchema.value === '') {
    router.push({ name: 'home' });
  }
});

// 处理配置加载成功
const handleLoaded = (config: any) => {
  configData.value = config;
  // 设置文档标题
  if (config && config.title) {
    document.title = config.title;
  }
};

// 处理加载错误
const handleError = (err: any) => {
  error.value = err;
  console.error('Failed to load SDUI config:', err);
};
</script>

<style scoped>
.sdui-view {
  width: 100%;
  min-height: calc(100vh - 64px);
}
</style>