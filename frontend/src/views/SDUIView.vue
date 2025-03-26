<template>
  <div class="sdui-view">
    <div v-if="uiStore.isLoading" class="loading">
      <p>Loading UI configuration...</p>
    </div>
    
    <div v-else-if="uiStore.errorMessage" class="error">
      <h2>Error Loading UI</h2>
      <p>{{ uiStore.errorMessage }}</p>
      <button @click="handleRetry">Retry</button>
    </div>
    
    <div v-else-if="uiConfig" class="renderer-container">
      <h1>{{ uiConfig.screen?.title || 'SDUI Screen' }}</h1>
      
      <div class="debug-info">
        <p><strong>Screen ID:</strong> {{ screenId }}</p>
        <p><strong>UI配置数据类型:</strong> {{ typeof uiConfig }}</p>
      </div>
      
      <!-- 这里将来会使用动态组件渲染 -->
      <div class="component-placeholder">
        <pre>{{ JSON.stringify(uiConfig, null, 2) }}</pre>
      </div>
    </div>
    
    <div v-else class="error">
      <p>No UI configuration available.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUIStore } from '../stores/uiStore';

const route = useRoute();
const uiStore = useUIStore();

// 获取当前路由中的屏幕ID
const screenId = computed(() => route.params.screenId as string);

// 获取当前UI配置
const uiConfig = computed(() => uiStore.currentScreen);

// 加载屏幕配置
const loadScreen = async (forceRefresh = false) => {
  try {
    console.log(`SDUIView - 开始加载屏幕 ${screenId.value}`);
    await uiStore.loadScreen(screenId.value, forceRefresh);
    console.log(`SDUIView - 屏幕加载完成:`, uiStore.currentScreen);
  } catch (error) {
    console.error('SDUIView - 加载屏幕失败:', error);
  }
};

// 重试按钮处理函数
const handleRetry = () => {
  loadScreen(true);
};

// 监听路由变化，加载新屏幕
watch(screenId, () => {
  loadScreen();
});

// 组件挂载时加载屏幕
onMounted(() => {
  loadScreen();
});
</script>

<style scoped>
.sdui-view {
  padding: 1rem;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #d32f2f;
}

.component-placeholder {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: auto;
}

pre {
  margin: 0;
  text-align: left;
}
</style> 