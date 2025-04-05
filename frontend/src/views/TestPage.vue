<template>
  <div class="test-page">
    <h2>SDUI渲染测试</h2>
    
    <!-- 应用布局测试 -->
    <div class="test-section">
      <h3>1. 应用布局测试</h3>
      <AppHeader v-bind="headerProps" />
      <div class="layout-container">
        <AppSider v-bind="siderProps" />
        <TabsContent :mode="contentProps.tabMode" />
      </div>
    </div>

    <!-- 页面配置测试 -->
    <div class="test-section">
      <h3>2. 商品流通工作台页面测试</h3>
      <div class="page-container">
        <SDUIRenderer :config="productFlowConfig" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import AppHeader from '@/layouts/components/AppHeader.vue';
import AppSider from '@/layouts/components/AppSider.vue';
import TabsContent from '@/layouts/components/TabsContent.vue';
import SDUIRenderer from '@/core/components/SDUIRenderer.vue';
import { mockAppConfig } from '@/services/mock/app-config';
import { mockProductFlowConfig } from '@/services/mock/page-config';

// 从mockAppConfig中提取布局配置
const headerProps = computed(() => ({
  ...mockAppConfig.layout.header,
  ...mockAppConfig.layout.header.components
}));

const siderProps = computed(() => ({
  ...mockAppConfig.layout.sider,
  menuItems: mockAppConfig.router.routes
}));

const contentProps = computed(() => mockAppConfig.layout.content);

// 页面配置
const productFlowConfig = computed(() => mockProductFlowConfig);
</script>

<style scoped>
.test-page {
  padding: 20px;
}

.test-section {
  margin-bottom: 40px;
  border: 1px solid #f0f0f0;
  padding: 20px;
  border-radius: 4px;
}

.test-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #1890ff;
}

.layout-container {
  display: flex;
  min-height: 500px;
  border: 1px solid #f0f0f0;
  margin-top: 20px;
}

.page-container {
  background: #fff;
  min-height: 400px;
  padding: 24px;
  border-radius: 4px;
}
</style> 