<template>
  <div 
    class="sd-list" 
    :style="style"
    ref="listContainerRef"
  >
    <div v-if="properties.title" class="sd-list-title">
      {{ properties.title }}
    </div>
    
    <!-- 列表项容器 -->
    <div 
      class="sd-list-items" 
      :class="{ 'sd-list-loading': loading && items.length > 0 }"
      @scroll="handleScroll"
    >
      <div v-if="items.length === 0 && !loading" class="sd-list-empty">
        {{ properties.emptyText || '暂无数据' }}
      </div>
      
      <div v-for="(item, index) in items" 
        :key="item.id || index" 
        class="sd-list-item"
        :class="{ 
          'sd-list-item-clickable': hasItemClick,
          'sd-list-item-selected': selectedIndex === index
        }"
        @click="handleItemClick(item, index)"
      >
        <!-- 默认渲染 -->
        <template v-if="!hasCustomRender">
          <div class="sd-list-item-content">
            <div class="sd-list-item-title">{{ item[properties.titleField || 'title'] }}</div>
            <div v-if="properties.descriptionField && item[properties.descriptionField]" 
              class="sd-list-item-description">
              {{ item[properties.descriptionField] }}
            </div>
          </div>
        </template>
        
        <!-- 自定义渲染 -->
        <slot v-else :item="item" :index="index"></slot>
      </div>
      
      <!-- 加载中状态 -->
      <div v-if="loading" class="sd-list-loading-indicator">
        <div class="sd-list-spinner"></div>
        <span>加载中...</span>
      </div>
      
      <!-- 全部加载完毕 -->
      <div v-if="!loading && !canLoadMore && items.length > 0" class="sd-list-end">
        {{ properties.endText || '已经到底了' }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue';

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
const items = ref<any[]>([]);
const page = ref(1);
const canLoadMore = ref(true);
const selectedIndex = ref(-1);
const listContainerRef = ref<HTMLElement | null>(null);

// 计算属性
const hasItemClick = computed(() => !!props.events?.onItemClick || !!props.properties.onItemClick);
const hasCustomRender = computed(() => !!props.properties.customRender);
const pageSize = computed(() => props.properties.pageSize || 10);

// 初始化
onMounted(async () => {
  // 初始化数据
  if (props.properties.items) {
    // 如果已传入静态数据
    items.value = props.properties.items;
  } else {
    // 如果需要从API加载数据
    await loadData();
  }
});

// 处理滚动事件
const handleScroll = async (event: Event) => {
  if (!canLoadMore.value || loading.value) return;
  
  const target = event.target as HTMLElement;
  const { scrollTop, scrollHeight, clientHeight } = target;
  
  // 当滚动到底部附近时加载更多
  if (scrollHeight - scrollTop - clientHeight < 100) {
    await loadMore();
  }
};

// 加载更多数据
const loadMore = async () => {
  if (!canLoadMore.value || loading.value) return;
  
  page.value++;
  await loadData();
};

// 加载数据
const loadData = async () => {
  if (props.properties.static) {
    canLoadMore.value = false;
    return;
  }
  
  // 如果没有定义加载方法，则不执行
  if (!props.events?.onLoadData && !props.properties.onLoadData) {
    console.warn('List component: No load data method provided');
    canLoadMore.value = false;
    return;
  }
  
  try {
    loading.value = true;
    
    // 触发加载数据事件
    emit('action', {
      type: 'loadData',
      componentId: props.id,
      page: page.value,
      pageSize: pageSize.value,
      event: props.events?.onLoadData || props.properties.onLoadData
    });
    
    // 注意：实际数据应该通过事件回调获取
    // 这里模拟一个延迟来演示加载效果
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // 模拟数据获取
    if (props.properties.mockData) {
      const startIndex = (page.value - 1) * pageSize.value;
      const newItems = props.properties.mockData.slice(startIndex, startIndex + pageSize.value);
      
      if (newItems.length === 0) {
        canLoadMore.value = false;
      } else {
        items.value = [...items.value, ...newItems];
      }
    }
    
  } catch (error) {
    console.error('Failed to load list data:', error);
    emit('action', {
      type: 'error',
      componentId: props.id,
      error
    });
  } finally {
    loading.value = false;
  }
};

// 处理列表项点击
const handleItemClick = (item: any, index: number) => {
  selectedIndex.value = index;
  
  if (hasItemClick.value) {
    emit('action', {
      type: 'itemClick',
      componentId: props.id,
      item,
      index,
      event: props.events?.onItemClick || props.properties.onItemClick
    });
  }
};

// 重新加载数据
const refresh = async () => {
  items.value = [];
  page.value = 1;
  canLoadMore.value = true;
  await loadData();
};

// 监听属性变化
watch(() => props.properties.items, (newItems) => {
  if (newItems) {
    items.value = newItems;
  }
});

// 向父组件暴露方法
defineExpose({
  refresh,
  loadMore,
  items
});
</script>

<style scoped>
.sd-list {
  width: 100%;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
  background-color: #fff;
  color: #303133;
  transition: .3s;
}

.sd-list-title {
  padding: 12px 20px;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #ebeef5;
  background-color: #f5f7fa;
}

.sd-list-items {
  overflow-y: auto;
  max-height: 400px; /* 可自定义或从属性中获取 */
  position: relative;
}

.sd-list-item {
  padding: 12px 20px;
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.2s;
}

.sd-list-item:last-child {
  border-bottom: none;
}

.sd-list-item-clickable {
  cursor: pointer;
}

.sd-list-item-clickable:hover {
  background-color: #f5f7fa;
}

.sd-list-item-selected {
  background-color: #ecf5ff;
}

.sd-list-item-content {
  display: flex;
  flex-direction: column;
}

.sd-list-item-title {
  font-weight: 500;
  color: #303133;
}

.sd-list-item-description {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.sd-list-empty {
  padding: 30px 0;
  text-align: center;
  color: #909399;
}

.sd-list-loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 15px 0;
  color: #909399;
}

.sd-list-spinner {
  width: 20px;
  height: 20px;
  margin-right: 8px;
  border: 2px solid #409eff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: list-spinner 0.8s linear infinite;
}

.sd-list-end {
  text-align: center;
  padding: 10px 0;
  color: #909399;
  font-size: 12px;
}

@keyframes list-spinner {
  to {
    transform: rotate(360deg);
  }
}
</style> 