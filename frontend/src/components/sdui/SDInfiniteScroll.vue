<template>
  <div 
    class="sd-infinite-scroll" 
    :style="style"
    ref="scrollContainerRef"
    @scroll="handleScroll"
  >
    <!-- 内容区域 -->
    <div class="sd-infinite-scroll-content">
      <slot></slot>
      
      <!-- 加载中状态 -->
      <div v-if="loading" class="sd-infinite-scroll-loading">
        <div class="sd-infinite-scroll-spinner"></div>
        <span>{{ properties.loadingText || '加载中...' }}</span>
      </div>
      
      <!-- 全部加载完毕 -->
      <div v-if="!loading && !hasMore" class="sd-infinite-scroll-end">
        {{ properties.endText || '已经到底了' }}
      </div>
      
      <!-- 加载错误 -->
      <div v-if="error" class="sd-infinite-scroll-error">
        <span>{{ properties.errorText || '加载失败' }}</span>
        <button 
          class="sd-infinite-scroll-retry" 
          @click="loadMore"
        >
          {{ properties.retryText || '重试' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

// 定义组件属性
const props = defineProps({
  id: {
    type: String,
    required: true
  },
  properties: {
    type: Object,
    default: () => ({})
  },
  style: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  }
});

// 定义事件
const emit = defineEmits(['action']);

// 内部状态
const loading = ref(false);
const hasMore = ref(true);
const error = ref(false);
const page = ref(1);
const scrollContainerRef = ref<HTMLElement | null>(null);

// 处理滚动事件
const handleScroll = () => {
  if (!hasMore.value || loading.value) return;
  
  const container = scrollContainerRef.value;
  if (!container) return;
  
  // 判断是否滚动到底部
  const { scrollTop, scrollHeight, clientHeight } = container;
  const threshold = props.properties.threshold || 100;
  
  if (scrollHeight - scrollTop - clientHeight < threshold) {
    loadMore();
  }
};

// 加载更多数据
const loadMore = async () => {
  if (loading.value || !hasMore.value) return;
  
  try {
    loading.value = true;
    error.value = false;
    
    // 触发加载事件
    if (props.events?.onLoadMore || props.properties.onLoadMore) {
      emit('action', {
        type: 'loadMore',
        componentId: props.id,
        page: page.value,
        event: props.events?.onLoadMore || props.properties.onLoadMore
      });
    } else {
      console.warn('InfiniteScroll component: No load more handler provided');
      hasMore.value = false;
      return;
    }
    
    // 在实际应用中，服务器响应将决定 hasMore
    // 这里模拟加载更多的逻辑
    await new Promise<void>((resolve) => {
      setTimeout(() => {
        if (props.properties.maxPage && page.value >= props.properties.maxPage) {
          hasMore.value = false;
        }
        page.value++;
        resolve();
      }, 800);
    });
    
  } catch (err) {
    console.error('Failed to load more data:', err);
    error.value = true;
    
    // 触发错误事件
    emit('action', {
      type: 'error',
      componentId: props.id,
      error: err
    });
  } finally {
    loading.value = false;
  }
};

// 重置组件状态
const reset = () => {
  page.value = 1;
  hasMore.value = true;
  error.value = false;
  
  // 触发重置事件
  emit('action', {
    type: 'reset',
    componentId: props.id
  });
};

// 手动检查是否需要加载更多
const checkPosition = () => {
  // 如果容器还有空间，并且有更多数据，则自动加载
  const container = scrollContainerRef.value;
  if (!container) return;
  
  const { scrollHeight, clientHeight } = container;
  if (clientHeight >= scrollHeight && hasMore.value && !loading.value) {
    loadMore();
  }
};

// 使用 IntersectionObserver 优化滚动检测
let observer: IntersectionObserver | null = null;

// 初始化监视器
const initObserver = () => {
  if (!window.IntersectionObserver) return;
  
  const options = {
    root: scrollContainerRef.value,
    rootMargin: `${props.properties.threshold || 100}px`,
    threshold: 0
  };
  
  const target = document.createElement('div');
  target.className = 'sd-infinite-scroll-observer';
  scrollContainerRef.value?.appendChild(target);
  
  observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && hasMore.value && !loading.value) {
      loadMore();
    }
  }, options);
  
  observer.observe(target);
};

// 生命周期钩子
onMounted(() => {
  // 如果支持 IntersectionObserver，则使用它
  if (window.IntersectionObserver && props.properties.useObserver !== false) {
    initObserver();
  }
  
  // 初始检查是否需要加载数据
  checkPosition();
});

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
    observer = null;
  }
});

// 监听属性变化
watch(() => props.properties.resetTrigger, () => {
  reset();
});

// 向父组件暴露方法
defineExpose({
  loadMore,
  reset
});
</script>

<style scoped>
.sd-infinite-scroll {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  position: relative;
}

.sd-infinite-scroll-content {
  min-height: 100%;
}

.sd-infinite-scroll-loading,
.sd-infinite-scroll-end,
.sd-infinite-scroll-error {
  padding: 16px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.sd-infinite-scroll-loading {
  display: flex;
  align-items: center;
  justify-content: center;
}

.sd-infinite-scroll-spinner {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  border: 2px solid #409eff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: infinite-scroll-spinner 0.8s linear infinite;
}

.sd-infinite-scroll-error {
  color: #f56c6c;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.sd-infinite-scroll-retry {
  padding: 4px 12px;
  font-size: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background-color: #fff;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s ease;
}

.sd-infinite-scroll-retry:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.sd-infinite-scroll-observer {
  height: 1px;
  width: 100%;
  position: relative;
  visibility: hidden;
}

@keyframes infinite-scroll-spinner {
  to {
    transform: rotate(360deg);
  }
}
</style> 