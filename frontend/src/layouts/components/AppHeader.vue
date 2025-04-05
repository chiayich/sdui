<template>
  <header class="app-header" :class="{ 'header-fixed': fixed }">
    <div class="header-logo">
      <img :src="logo.src" :alt="logo.alt" />
    </div>
    <div class="header-content">
      <div class="global-search" v-if="globalSearch">
        <input
          :placeholder="globalSearch.placeholder"
          :style="{ width: globalSearch.width + 'px' }"
        />
      </div>
    </div>
    <div class="header-right">
      <div class="user-info">
        <img v-if="userInfo.avatar" :src="userInfo.avatar" class="avatar" />
        <span class="username">{{ userInfo.name }}</span>
        <span class="role">{{ userInfo.role }}</span>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { LogoConfig, UserInfoConfig, SearchConfig } from '@/core/types/framework';

defineProps<{
  fixed?: boolean;
  height?: number;
  logo: LogoConfig;
  userInfo: UserInfoConfig;
  globalSearch?: SearchConfig;
}>();
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  background: #001529;
  color: white;
  height: v-bind(height + 'px' || '64px');
}

.header-fixed {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.header-logo {
  display: flex;
  align-items: center;
}

.header-logo img {
  height: 32px;
}

.header-content {
  flex: 1;
  display: flex;
  align-items: center;
  margin: 0 24px;
}

.global-search input {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  padding: 4px 12px;
  color: white;
  border-radius: 4px;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  margin-right: 8px;
}

.username {
  margin-right: 8px;
}

.role {
  opacity: 0.8;
  font-size: 12px;
}
</style> 