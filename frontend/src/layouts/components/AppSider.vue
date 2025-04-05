<template>
  <aside
    class="app-sider"
    :class="[
      `theme-${theme}`,
      { 'sider-collapsed': collapsed }
    ]"
    :style="{ width: collapsed ? '80px' : width + 'px' }"
  >
    <div class="menu-container">
      <template v-for="item in menuItems" :key="item.id">
        <!-- 一级菜单 -->
        <div
          v-if="!item.children"
          class="menu-item"
          :class="{ active: currentPath === item.path }"
          @click="handleMenuClick(item)"
        >
          <i v-if="item.icon" :class="item.icon"></i>
          <span v-if="!collapsed" class="menu-title">{{ item.title }}</span>
        </div>
        
        <!-- 二级菜单 -->
        <div v-else class="submenu">
          <div class="submenu-title" @click="toggleSubmenu(item)">
            <i v-if="item.icon" :class="item.icon"></i>
            <span v-if="!collapsed" class="menu-title">{{ item.title }}</span>
            <i
              v-if="!collapsed"
              class="arrow"
              :class="{ expanded: expandedMenus.includes(item.id) }"
            ></i>
          </div>
          <div
            v-show="!collapsed && expandedMenus.includes(item.id)"
            class="submenu-items"
          >
            <div
              v-for="subItem in item.children"
              :key="subItem.id"
              class="menu-item"
              :class="{ active: currentPath === subItem.path }"
              @click="handleMenuClick(subItem)"
            >
              <span class="menu-title">{{ subItem.title }}</span>
            </div>
          </div>
        </div>
      </template>
    </div>
    
    <div class="sider-trigger" @click="toggleCollapse">
      <i :class="collapsed ? 'trigger-right' : 'trigger-left'"></i>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { RouteConfig } from '@/core/types/framework';

const props = defineProps<{
  width: number;
  theme: 'light' | 'dark';
  menuItems: RouteConfig[];
}>();

const router = useRouter();
const route = useRoute();

const collapsed = ref(false);
const expandedMenus = ref<string[]>([]);
const currentPath = computed(() => route.path);

const toggleCollapse = () => {
  collapsed.value = !collapsed.value;
};

const toggleSubmenu = (item: RouteConfig) => {
  const index = expandedMenus.value.indexOf(item.id);
  if (index > -1) {
    expandedMenus.value.splice(index, 1);
  } else {
    expandedMenus.value.push(item.id);
  }
};

const handleMenuClick = (item: RouteConfig) => {
  router.push(item.path);
};
</script>

<style scoped>
.app-sider {
  height: 100%;
  transition: width 0.2s;
  position: relative;
  overflow: hidden;
}

.theme-dark {
  background: #001529;
  color: rgba(255, 255, 255, 0.65);
}

.theme-light {
  background: #fff;
  color: rgba(0, 0, 0, 0.65);
  border-right: 1px solid #f0f0f0;
}

.menu-container {
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

.menu-item {
  padding: 0 24px;
  height: 40px;
  line-height: 40px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}

.theme-dark .menu-item:hover {
  color: #fff;
}

.theme-light .menu-item:hover {
  color: #1890ff;
}

.menu-item.active {
  color: #1890ff;
  background: #e6f7ff;
}

.menu-title {
  margin-left: 10px;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.submenu-title {
  padding: 0 24px;
  height: 40px;
  line-height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.arrow {
  margin-left: auto;
  transition: transform 0.2s;
}

.arrow.expanded {
  transform: rotate(90deg);
}

.submenu-items {
  background: rgba(0, 0, 0, 0.02);
}

.sider-trigger {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 2px;
  cursor: pointer;
}

.theme-dark .sider-trigger {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.theme-light .sider-trigger {
  background: #fff;
  color: #001529;
  border: 1px solid #f0f0f0;
}
</style> 