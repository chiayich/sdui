import { defineStore } from 'pinia';
import api from '../lib/api';

interface UIState {
  screens: Record<string, any>;
  loading: boolean;
  error: string | null;
  currentScreenId: string | null;
}

export const useUIStore = defineStore('ui', {
  state: (): UIState => ({
    screens: {},
    loading: false,
    error: null,
    currentScreenId: null
  }),
  
  getters: {
    // 获取当前屏幕配置
    currentScreen: (state): any | null => {
      if (!state.currentScreenId) return null;
      return state.screens[state.currentScreenId] || null;
    },
    
    // 检查是否正在加载
    isLoading: (state): boolean => state.loading,
    
    // 获取错误信息
    errorMessage: (state): string | null => state.error
  },
  
  actions: {
    // 加载屏幕配置
    async loadScreen(screenId: string, forceRefresh = false) {
      // 如果已有缓存且不强制刷新，则使用缓存数据
      if (!forceRefresh && this.screens[screenId]) {
        this.currentScreenId = screenId;
        return this.screens[screenId];
      }
      
      this.loading = true;
      this.error = null;
      
      try {
        console.log(`尝试加载屏幕配置: ${screenId}`);
        const response = await api.uiTemplates.getScreenConfig(screenId);
        console.log(`获取屏幕配置成功:`, response);
        
        // 存储屏幕配置 - 注意API响应可能直接就是数据本身
        const screenConfig = response.data || response;
        console.log(`处理后的屏幕配置:`, screenConfig);
        
        this.screens[screenId] = screenConfig;
        this.currentScreenId = screenId;
        
        return screenConfig;
      } catch (error: any) {
        // 处理错误
        this.error = error.message || 'Failed to load screen configuration';
        console.error(`Failed to load screen ${screenId}:`, error);
        
        // 回退到Mock数据（仅开发环境）
        if (import.meta.env.DEV && screenId === 'home') {
          const mockConfig = this.getMockScreenConfig(screenId);
          this.screens[screenId] = mockConfig;
          return mockConfig;
        }
        
        throw error;
      } finally {
        this.loading = false;
      }
    },
    
    // 清除特定屏幕缓存
    clearScreenCache(screenId: string) {
      if (this.screens[screenId]) {
        delete this.screens[screenId];
      }
    },
    
    // 清除所有缓存
    clearAllCache() {
      this.screens = {};
    },
    
    // 获取Mock数据（仅开发环境）
    getMockScreenConfig(screenId: string) {
      if (screenId === 'home') {
        return {
          version: "1.0.0",
          screen: {
            id: "home",
            title: "Home Screen",
            components: [
              {
                type: "container",
                id: "main-container",
                style: {"padding": 16},
                children: [
                  {
                    type: "text",
                    id: "welcome-text",
                    content: "Welcome to SDUI",
                    style: {"fontSize": 24, "fontWeight": "bold"}
                  },
                  {
                    type: "button",
                    id: "action-button",
                    label: "Click Me",
                    style: {"marginTop": 16},
                    action: {"type": "navigate", "target": "detail"}
                  }
                ]
              }
            ]
          }
        };
      }
      
      return null;
    }
  }
}); 