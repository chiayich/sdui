<template>
  <div class="tabs-content">
    <div class="tabs-bar">
      <div
        v-for="tab in tabs"
        :key="tab.pageKey"
        class="tab-item"
        :class="{ active: currentTab === tab.pageKey }"
        @click="switchTab(tab.pageKey)"
      >
        <span class="tab-title">{{ tab.title }}</span>
        <span
          v-if="tab.closeable !== false"
          class="tab-close"
          @click.stop="closeTab(tab.pageKey)"
        >
          ×
        </span>
      </div>
    </div>
    
    <div class="content-container">
      <component
        v-for="tab in tabs"
        :key="tab.pageKey"
        :is="tab.component"
        v-show="currentTab === tab.pageKey"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Component } from 'vue';

interface Tab {
  pageKey: string;
  title: string;
  closeable?: boolean;
  component: Component;
}

const props = defineProps<{
  mode: 'multi' | 'single';
}>();

const tabs = ref<Tab[]>([]);
const currentTab = ref<string>('');
const route = useRoute();
const router = useRouter();

// 监听路由变化
watch(
  () => route.meta,
  async (meta) => {
    if (meta.pageKey) {
      const component = route.matched[route.matched.length - 1].components?.default;
      if (component) {
        await addTab({
          pageKey: meta.pageKey as string,
          title: meta.title as string,
          component
        });
      }
    }
  },
  { immediate: true }
);

const addTab = async (tab: Tab) => {
  const existingTab = tabs.value.find(t => t.pageKey === tab.pageKey);
  if (!existingTab) {
    if (props.mode === 'single') {
      tabs.value = [tab];
    } else {
      tabs.value.push(tab);
    }
  }
  currentTab.value = tab.pageKey;
};

const switchTab = (pageKey: string) => {
  const tab = tabs.value.find(t => t.pageKey === pageKey);
  if (tab) {
    currentTab.value = pageKey;
    router.push({ name: pageKey });
  }
};

const closeTab = (pageKey: string) => {
  const index = tabs.value.findIndex(t => t.pageKey === pageKey);
  if (index > -1) {
    tabs.value.splice(index, 1);
    if (currentTab.value === pageKey) {
      if (tabs.value.length) {
        // 切换到前一个或后一个标签
        const nextTab = tabs.value[index] || tabs.value[index - 1];
        if (nextTab) {
          switchTab(nextTab.pageKey);
        }
      } else {
        router.push('/');
      }
    }
  }
};
</script>

<style scoped>
.tabs-content {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.tabs-bar {
  height: 40px;
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  padding: 0 16px;
  overflow-x: auto;
}

.tab-item {
  padding: 0 16px;
  height: 40px;
  line-height: 40px;
  background: #fafafa;
  border: 1px solid #f0f0f0;
  border-bottom: none;
  margin-right: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-radius: 4px 4px 0 0;
}

.tab-item.active {
  background: #fff;
  border-bottom: 2px solid #1890ff;
  color: #1890ff;
}

.tab-title {
  margin-right: 8px;
}

.tab-close {
  width: 16px;
  height: 16px;
  line-height: 16px;
  text-align: center;
  border-radius: 50%;
  font-size: 12px;
}

.tab-close:hover {
  background: rgba(0, 0, 0, 0.1);
}

.content-container {
  flex: 1;
  overflow: auto;
  background: #fff;
  padding: 24px;
}
</style> 