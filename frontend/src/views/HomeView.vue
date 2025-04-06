<template>
  <div class="home">
    <div v-if="sduiStore.isLoading" class="loading-indicator">
      <div class="spinner"></div>
      <p>加载页面中...</p>
    </div>
    <div v-else-if="sduiStore.error" class="error-container">
      <h3>加载错误</h3>
      <p>{{ sduiStore.error }}</p>
      <button @click="handleRetry">重试</button>
    </div>
    <div v-else-if="!pageConfig" class="error-container">
      <h3>页面配置为空</h3>
      <p>服务器返回的配置为空</p>
      <button @click="reloadConfig()">加载首页</button>
    </div>
    <div v-else>
      <div class="debug-banner" v-if="isDebug">
        加载的页面配置: {{ pageConfig.type || '未知类型' }} - {{ pageConfig.title || '无标题' }}
        <button class="debug-button" @click="toggleConfig">查看配置</button>
      </div>
      <div v-if="showConfig && isDebug" class="config-preview">
        <pre>{{ JSON.stringify(pageConfig, null, 2) }}</pre>
      </div>
      <component-renderer :component="pageConfig" :context="context" @action="handleAction" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, inject, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useSduiStore } from '@/stores/sduiStore';
import ComponentRenderer from '@/components/sdui/ComponentRenderer.vue';

const router = useRouter();
const sduiStore = useSduiStore();

// 调试状态
const isDebug = ref(import.meta.env.DEV && (import.meta.env.VITE_DEBUG === 'true' || true));
const showConfig = ref(false);

// 从Store获取页面配置
const pageConfig = computed(() => {
  if (sduiStore.homeConfig) {
    console.log('HomeView: 使用缓存的首页配置');
    return sduiStore.homeConfig;
  }
  console.log('HomeView: 首页配置不存在');
  return null;
});

// 监听首页配置变化
watch(() => sduiStore.homeConfig, (newConfig) => {
  if (newConfig) {
    console.log('HomeView: 首页配置已更新:', {
      type: newConfig.type,
      title: newConfig.title,
      组件数量: newConfig.components?.length || 0
    });
  } else {
    console.log('HomeView: 首页配置被清除');
  }
});

// 获取全局上下文，或创建一个新的
const globalContext = inject('globalContext', {}) as any;
const context = reactive({
  ...globalContext,
  // 添加首页特定上下文
  page: 'home'
});

// 加载/重载首页配置
const reloadConfig = (force = false) => {
  console.log(`HomeView: 请求${force ? '强制' : ''}加载首页配置`);
  sduiStore.loadHomeConfig(force);
};

// 处理重试按钮点击
const handleRetry = () => {
  reloadConfig(true);
};

// 处理组件动作
const handleAction = (action: any) => {
  console.log('首页动作:', action);

  if (action.type === 'navigation' && action.url) {
    router.push(action.url);
  }
};

// 切换配置显示
const toggleConfig = () => {
  showConfig.value = !showConfig.value;
};

// 组件挂载时检查配置
onMounted(() => {
  // 在挂载时，如果没有首页配置，才请求加载
  if (!sduiStore.isHomeLoaded) {
    console.log('HomeView: 首页配置尚未加载，发起请求');
    reloadConfig();
  } else {
    console.log('HomeView: 首页配置已加载，使用现有配置');

    // 如果是调试模式，输出配置信息
    if (isDebug.value) {
      console.log('HomeView 调试信息:', {
        配置类型: pageConfig.value?.type,
        配置标题: pageConfig.value?.title,
        组件数量: pageConfig.value?.components?.length || 0
      });
    }
  }
});
</script>

<style scoped>
.home {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  margin-top: 50px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

.error-container {
  padding: 24px;
  border: 1px solid #f56c6c;
  background-color: #fef0f0;
  border-radius: 4px;
  text-align: center;
  margin: 24px;
  max-width: 600px;
}

.error-container button {
  margin-top: 16px;
  padding: 8px 16px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.debug-banner {
  background-color: #e6f7ff;
  color: #1890ff;
  padding: 8px 16px;
  margin-bottom: 16px;
  border-radius: 4px;
  text-align: center;
  width: 100%;
  font-size: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.debug-button {
  background-color: #1890ff;
  color: white;
  padding: 2px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.config-preview {
  max-height: 300px;
  overflow: auto;
  background-color: #f9f9f9;
  padding: 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  margin-bottom: 16px;
  width: 100%;
}

.config-preview pre {
  margin: 0;
  font-family: monospace;
  font-size: 12px;
  color: #333;
  white-space: pre-wrap;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>