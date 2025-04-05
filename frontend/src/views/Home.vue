<template>
  <div class="home">
    <SDUIRenderer
      :config="homeConfig"
      @state-change="handleStateChange"
      @refresh="handleRefresh"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import SDUIRenderer from '@/core/components/SDUIRenderer.vue';
import { mockHomeConfig } from '@/services/mock/home-config';

type StateValue = string | number;

interface PageState {
  currentStore: string;
  refreshKey: number;
}

// 页面状态
const pageState = ref<PageState>({
  currentStore: '',
  refreshKey: 0
});

// 页面配置
const homeConfig = computed(() => ({
  ...mockHomeConfig,
  state: {
    ...mockHomeConfig.state,
    currentStore: {
      type: 'string',
      default: pageState.value.currentStore
    }
  }
}));

// 处理状态变化
const handleStateChange = (key: string, value: StateValue) => {
  if (key in pageState.value) {
    (pageState.value as any)[key] = value;
  }
};

// 处理刷新
const handleRefresh = () => {
  pageState.value.refreshKey++;
};
</script>

<style scoped>
.home {
  padding: 24px;
  background: #f0f2f5;
  min-height: 100vh;
}
</style> 