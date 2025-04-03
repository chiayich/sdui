<template>
  <div class="sdui-view">
    <div v-if="uiStore.isLoading" class="loading">
      <p>加载UI配置中...</p>
    </div>
    
    <div v-else-if="uiStore.errorMessage" class="error">
      <h2>加载UI出错</h2>
      <p>{{ uiStore.errorMessage }}</p>
      <button @click="handleRetry">重试</button>
    </div>
    
    <div v-else-if="uiConfig" class="renderer-container">
      <div class="screen-header">
        <h1>{{ uiConfig.screen?.title || 'SDUI 屏幕' }}</h1>
      </div>
      
      <div class="debug-info" v-if="showDebug">
        <p><strong>屏幕ID:</strong> {{ screenId }}</p>
        <p><strong>配置版本:</strong> {{ uiConfig.version || '未指定' }}</p>
        <button @click="toggleDebug">{{ showDebug ? '隐藏' : '显示' }}JSON</button>
        <pre v-if="showJson">{{ JSON.stringify(uiConfig, null, 2) }}</pre>
      </div>
      
      <!-- 使用SDUI渲染器组件 -->
      <SDUIRenderer :config="uiConfig" />
    </div>
    
    <div v-else class="error">
      <p>没有可用的UI配置。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useUIStore } from '../stores/uiStore';
import SDUIRenderer from '../components/SDUIRenderer.vue';

const route = useRoute();
const uiStore = useUIStore();

// 获取当前路由中的屏幕ID
const screenId = computed(() => route.params.screenId as string);

// 获取当前UI配置
const uiConfig = computed(() => uiStore.currentScreen);

// 调试状态
const showDebug = ref(false);
const showJson = ref(false);

// 切换调试信息显示
const toggleDebug = () => {
  showJson.value = !showJson.value;
};

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
  max-width: 1200px;
  margin: 0 auto;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
}

.error {
  color: #d32f2f;
}

.screen-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.debug-info {
  margin: 1rem 0;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 4px;
  border: 1px solid #eee;
}

.debug-info button {
  margin: 0.5rem 0;
  padding: 0.25rem 0.5rem;
}

.debug-info pre {
  margin: 0.5rem 0 0;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
  overflow: auto;
  text-align: left;
}

.renderer-container {
  margin-top: 1rem;
}
</style> 