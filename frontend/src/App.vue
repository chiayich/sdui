<template>
  <div id="app">
    <header v-if="sduiStore.isStructureLoaded">
      <nav-menu :config="sduiStore.navigationConfig" />
    </header>

    <main>
      <router-view />
    </main>

    <footer v-if="sduiStore.isStructureLoaded">
      <!-- 全局组件渲染 -->
      <div v-for="(component, index) in sduiStore.globalComponents" :key="`global-${index}`">
        <component-renderer :component="component" :context="globalContext" @action="handleGlobalAction" />
      </div>
    </footer>

    <!-- 全局加载中状态 -->
    <div v-if="sduiStore.isLoading" class="global-loader">
      <div class="loader-spinner"></div>
      <p>加载系统配置...</p>
    </div>

    <!-- 全局错误状态 -->
    <div v-if="!sduiStore.isLoading && sduiStore.error" class="global-error">
      <h3>系统加载出错</h3>
      <p>{{ sduiStore.error }}</p>
      <button @click="() => sduiStore.loadStructure(true)">重试</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted, watch, provide } from 'vue';
import { useAuthStore } from './stores/authStore';
import { useSduiStore } from './stores/sduiStore';
import { useRouter, useRoute } from 'vue-router';
import NavMenu from '@/components/NavMenu.vue';
import ComponentRenderer from '@/components/sdui/ComponentRenderer.vue';
import { UserInfoResponse } from './api/auth';

// 获取路由和状态
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const sduiStore = useSduiStore();

// 全局上下文对象
const globalContext = reactive({
  user: null as UserInfoResponse | null,
  theme: 'light',
});

// 监听认证状态变化
watch(() => authStore.user, (newUser) => {
  // 更新全局上下文中的用户信息
  globalContext.user = newUser;
}, { immediate: true });

// 提供全局上下文，可被所有组件注入
provide('globalContext', globalContext);

// 处理全局组件动作
const handleGlobalAction = (action: any) => {
  console.log('全局组件动作:', action);

  // 处理主题切换
  if (action.type === 'toggleTheme') {
    globalContext.theme = globalContext.theme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', globalContext.theme);
  }
};

// 确保应用正确初始化
onMounted(async () => {
  // 确保SDUI状态已初始化
  await sduiStore.initialize();
  console.log('App.vue: SDUI初始化完成', {
    已加载结构: sduiStore.isStructureLoaded,
    导航菜单项数: sduiStore.navigationConfig?.menuItems?.length || 0
  });
});
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
  color: #333;
  line-height: 1.6;
  background-color: #f0f2f5;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main {
  flex: 1;
  width: 100%;
}

.global-loader,
.global-error {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 1000;
}

.loader-spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

.global-error {
  color: #e74c3c;
}

.global-error button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
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