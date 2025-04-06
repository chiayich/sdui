<template>
  <div class="sdui-renderer" :class="{ 'admin-layout': config.layout?.type === 'admin' }">
    <!-- 管理系统布局 -->
    <template v-if="config.layout?.type === 'admin'">
      <!-- 顶部导航 -->
      <div v-if="config.layout?.header" class="admin-header header_bar" :style="config.layout.header.style">
        <div class="header-left">
          <div class="logo_con">
            <img v-if="config.layout.header.logo" :src="config.layout.header.logo" class="logo" alt="Logo" />
          </div>
          <h1 class="header-title">{{ config.layout.header.title }}</h1>
        </div>
        <div class="header-right">
          <div v-if="config.layout.header.userInfo" class="user-info">
            <span class="user-name">{{ config.layout.header.userInfo.name }}</span>
            <span class="user-role">{{ config.layout.header.userInfo.role }}</span>
          </div>
        </div>
      </div>

      <div class="admin-container">
        <!-- 左侧菜单 -->
        <div v-if="config.layout?.sider" class="admin-sider" :style="{ width: `${config.layout.sider.width}px` }">
          <div class="sider-menu">
            <template v-for="item in config.layout.sider.menu" :key="item.key">
              <div class="menu-item"
                :class="{ 'active': item.active || isActiveParent(item), 'has-children': item.children }"
                @click="handleMenuClick(item)" :data-title="item.title">
                <i v-if="item.icon" :class="item.icon"></i>
                <span>{{ item.title }}</span>
                <span v-if="item.children" class="menu-arrow" :class="{ 'expanded': item.expanded }">▶</span>
              </div>
              <div v-if="item.children && (item.expanded || isActiveParent(item))" class="sub-menu">
                <div v-for="child in item.children" :key="child.key" class="menu-item"
                  :class="{ 'active': child.active }" @click.stop="handleMenuClick(child)" :data-title="child.title">
                  <span>{{ child.title }}</span>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- 主内容区 -->
        <div class="admin-content">
          <template v-for="component in config.components" :key="component.id">
            <component :is="resolveComponent(component.type)" v-bind="resolveProps(component)"
              v-on="resolveEvents(component)" />
          </template>
        </div>
      </div>
    </template>

    <!-- 标准布局 -->
    <template v-else>
      <!-- 顶部标题 -->
      <div v-if="config.layout?.header" class="page-header" :style="config.layout.header.style">
        <h1 class="page-title">{{ config.layout.header.title }}</h1>
        <p v-if="config.layout.header.subtitle" class="page-subtitle">{{ config.layout.header.subtitle }}</p>
      </div>

      <!-- 主内容区 -->
      <div class="page-content">
        <template v-for="component in config.components" :key="component.id">
          <AsyncComponent :component-type="resolveComponent(component.type)" :component-data="component"
            @state-change="(key, value) => emit('state-change', key, value)" />
        </template>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, h, defineComponent } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { PageConfig, MenuItem } from '@/core/types/page';
import SDFilterBar from '@/core/components/SDFilterBar.vue';
import SDTable from '@/core/components/SDTable.vue';
import SDCard from '@/core/components/SDCard.vue';
import SDText from '@/core/components/SDText.vue';
import SDTabs from '@/core/components/SDTabs.vue';
import SDToolbar from '@/core/components/SDToolbar.vue';
import SDImageList from '@/core/components/SDImageList.vue';
import SDDatePicker from '@/core/components/form/SDDatePicker.vue';
import SDRow from '@/core/components/SDRow.vue';
import SDTags from '@/core/components/SDTags.vue';
import SDBarChart from '@/core/components/SDBarChart.vue';
import { sduiService } from '@/api/sdui';

// 组件映射表
const componentMap = {
  filterBar: SDFilterBar,
  table: SDTable,
  card: SDCard,
  text: SDText,
  tabs: SDTabs,
  toolbar: SDToolbar,
  imageList: SDImageList,
  input: 'input',
  datePicker: SDDatePicker,
  row: SDRow,
  tags: SDTags,
  barChart: SDBarChart,
  dropdown: 'select'
};

const props = defineProps<{
  config: PageConfig;
}>();

const emit = defineEmits<{
  'state-change': [key: string, value: any];
  'refresh': [];
}>();

const router = useRouter();
const route = useRoute();

// 页面状态
const pageState = ref<Record<string, any>>({});

// 数据源缓存
const dataSourceCache = ref<Record<string, any>>({});

// 初始化状态
const initState = () => {
  // 确保searchForm对象存在
  if (!pageState.value.searchForm) {
    pageState.value.searchForm = {
      flowDate: '2025-04-03',
      flowType: 'option1',
      bizType: '',
      goodsType: '',
      brand: ''
    };
  }

  // 初始化其他状态
  Object.entries(props.config.state || {}).forEach(([key, config]) => {
    if (!(key in pageState.value)) {
      pageState.value[key] = config.default;
    }
  });
};

// 监听配置变化，重新初始化状态
watch(() => props.config, () => {
  initState();
}, { immediate: true });

// 监听状态变化
watch(pageState, (newState, oldState) => {
  Object.entries(newState).forEach(([key, value]) => {
    if (value !== oldState[key]) {
      emit('state-change', key, value);
    }
  });
}, { deep: true });

// 解析组件类型
const resolveComponent = (type: string) => {
  return componentMap[type as keyof typeof componentMap] || 'div';
};

// 获取数据源
const getDataSource = async (source: string): Promise<any[]> => {
  // 如果缓存中有数据，直接返回
  if (dataSourceCache.value[source]) {
    return dataSourceCache.value[source];
  }

  // 从后端API获取数据
  try {
    const response = await sduiService.getConfig(`data/${source}`);
    const data = response.content || [];

    // 缓存数据
    dataSourceCache.value[source] = data;
    return data;
  } catch (error) {
    console.error(`Error fetching data source ${source}:`, error);
    return [];
  }
};

// 刷新数据源
const refreshDataSource = (source: string) => {
  // 清除缓存
  delete dataSourceCache.value[source];
  // 重新获取数据
  return getDataSource(source);
};

// 解析绑定值
const resolveBinding = async (binding: any) => {
  if (!binding) return null;

  switch (binding.type) {
    case 'state':
      return pageState.value[binding.source];
    case 'dataSource':
      try {
        return await getDataSource(binding.source);
      } catch (error) {
        console.error(`Error resolving binding for ${binding.source}:`, error);
        return [];
      }
    case 'compute':
      // 这里可以添加计算属性的支持
      return null;
    default:
      return null;
  }
};

// 解析组件属性
const resolveProps = async (component: any) => {
  const props = { ...component.props };

  // 处理数据绑定
  if (component.bindings) {
    for (const [key, binding] of Object.entries(component.bindings)) {
      props[key] = await resolveBinding(binding);
    }
  }

  return props;
};

// 解析组件事件
const resolveEvents = (component: any) => {
  const events: Record<string, Function> = {};

  if (component.events) {
    Object.entries(component.events).forEach(([event, handlers]) => {
      events[event] = (...args: any[]) => {
        if (Array.isArray(handlers)) {
          handlers.forEach(handler => {
            handleAction(handler, args);
          });
        }
      };
    });
  }

  // 添加值更新事件处理
  if (component.bindings) {
    Object.entries(component.bindings).forEach(([key, binding]: [string, any]) => {
      if (binding.type === 'state') {
        events[`update:${key}`] = (value: any) => {
          pageState.value[binding.source] = value;
        };
      }
    });
  }

  return events;
};

// 处理组件动作
const handleAction = (action: any, args: any[] = []) => {
  switch (action.type) {
    case 'state':
      switch (action.action) {
        case 'refreshData':
          // 刷新所有数据源
          Object.keys(props.config.dataSources || {}).forEach(source => {
            refreshDataSource(source);
          });
          emit('refresh');
          break;
        default:
          // 更新状态
          if (action.target && typeof action.value !== 'undefined') {
            pageState.value[action.target] = action.value;
          }
      }
      break;
    default:
      console.warn('未知动作类型:', action.type);
  }
};

// 检查菜单项是否为活动菜单的父级
const isActiveParent = (item: MenuItem) => {
  if (!item.children) return false;
  return item.children.some(child => child.active);
};

// 处理菜单点击事件
const handleMenuClick = (item: MenuItem) => {
  // 如果点击的是父菜单项且没有设置活动状态
  if (item.children && !item.active) {
    // 仅切换展开状态，不导航
    item.expanded = !item.expanded;
    return;
  }

  // 更新当前活动菜单项
  const updateActiveStatus = (menuList: MenuItem[]) => {
    menuList.forEach(menuItem => {
      // 重置所有菜单项的active状态
      menuItem.active = menuItem.key === item.key;

      // 处理子菜单
      if (menuItem.children) {
        const hasActiveChild = updateActiveStatus(menuItem.children);
        // 如果子菜单中有活动项，则将父菜单标记为展开状态
        if (hasActiveChild) {
          menuItem.expanded = true;
        }
      }
    });

    // 返回当前菜单列表中是否有活动项
    return menuList.some(menuItem => menuItem.active);
  };

  // 更新菜单状态
  if (props.config.layout?.sider?.menu) {
    updateActiveStatus([...props.config.layout.sider.menu]);
  }

  // 触发页面状态更新
  if (pageState.value.currentMenu !== item.key) {
    pageState.value.currentMenu = item.key;
    emit('state-change', 'currentMenu', item.key);

    // 使用vue-router进行导航
    switch (item.key) {
      case 'instruction':
        router.push('/flow/instruction');
        break;
      case 'simulation':
        router.push('/flow/simulation');
        break;
      case 'collection':
        router.push('/flow/collection');
        break;
      case 'workbench':
        router.push('/flow/workbench');
        break;
      case 'overview':
        router.push('/flow/overview');
        break;
    }
  }
};

// 在挂载时设置正确的活动菜单
onMounted(() => {
  // 获取当前路由路径
  const currentPath = route.path;

  // 根据路径找到对应的菜单键
  let menuKey = '';
  if (currentPath.includes('/flow/instruction')) {
    menuKey = 'instruction';
  } else if (currentPath.includes('/flow/simulation')) {
    menuKey = 'simulation';
  } else if (currentPath.includes('/flow/collection')) {
    menuKey = 'collection';
  } else if (currentPath.includes('/flow/workbench')) {
    menuKey = 'workbench';
  } else if (currentPath.includes('/flow/overview')) {
    menuKey = 'overview';
  }

  // 如果找到了菜单键，就更新菜单激活状态
  if (menuKey && props.config.layout?.sider?.menu) {
    const updateMenuActive = (menuList: MenuItem[]) => {
      menuList.forEach(menuItem => {
        if (menuItem.key === menuKey) {
          menuItem.active = true;
        } else {
          menuItem.active = false;
        }

        if (menuItem.children) {
          updateMenuActive(menuItem.children);
        }
      });
    };

    updateMenuActive([...props.config.layout.sider.menu]);

    // 更新当前菜单状态
    if (pageState.value.currentMenu !== menuKey) {
      pageState.value.currentMenu = menuKey;
    }
  }
});

// 初始化
initState();

// 创建异步组件包装器
const AsyncComponent = defineComponent({
  props: {
    componentType: {
      type: [String, Object],
      required: true
    },
    componentData: {
      type: Object,
      required: true
    }
  },
  emits: ['state-change'],
  data() {
    return {
      resolvedProps: {},
      loading: true,
      error: null as Error | null
    };
  },
  async created() {
    try {
      this.loading = true;
      this.resolvedProps = await resolveProps(this.componentData);
      this.loading = false;
    } catch (err: any) {
      this.error = err instanceof Error ? err : new Error(String(err));
      this.loading = false;
      console.error('Error resolving props:', err);
    }
  },
  render() {
    if (this.loading) {
      return h('div', { class: 'loading-component' }, '加载中...');
    }

    if (this.error) {
      return h('div', { class: 'error-component' }, `加载出错: ${this.error.message}`);
    }

    const events = resolveEvents(this.componentData);

    return h(this.componentType, {
      ...this.resolvedProps,
      ...events
    });
  }
});
</script>

<style scoped>
.sdui-renderer {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 管理系统布局样式 */
.admin-layout {
  background: #f0f2f5;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 48px;
  padding: 0 24px;
  background: #001529;
  color: #fff;
  position: relative;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo_con {
  display: inline-flex;
  align-items: center;
  margin-right: 16px;
}

.logo {
  height: 25px;
  width: 33px;
  vertical-align: middle;
}

.header-title {
  margin: 0;
  font-size: 18px;
  font-weight: 400;
  color: #fff;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-name {
  font-size: 14px;
}

.user-role {
  font-size: 12px;
  opacity: 0.8;
}

.admin-container {
  display: flex;
  flex: 1;
}

.admin-sider {
  background: #001529;
  color: #fff;
  min-height: calc(100vh - 48px);
  overflow-y: auto;
}

.sider-menu {
  padding: 0;
}

.menu-item {
  padding: 0 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  user-select: none;
  height: 50px;
  line-height: 50px;
  font-size: 14px;
  transition: all 0.3s;
  margin: 0;
}

.menu-item:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}

.menu-item.active {
  position: relative;
  background-color: #1890ff;
  color: #fff;
}

.menu-item.active span {
  color: #fff;
}

.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: #fff;
}

.sub-menu {
  background: rgba(0, 0, 0, 0.25);
}

.sub-menu .menu-item {
  padding-left: 48px;
  height: 50px;
  line-height: 50px;
}

.admin-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background: #f0f2f5;
}

/* 标准布局样式 */
.page-header {
  text-align: center;
  padding: 48px 0;
  background: #fff;
  margin-bottom: 24px;
}

.page-title {
  margin: 0;
  font-size: 32px;
  font-weight: 500;
  color: #000;
}

.page-subtitle {
  margin: 16px 0 0;
  font-size: 16px;
  color: #666;
}

.page-content {
  flex: 1;
  padding: 0 24px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.menu-item i {
  font-size: 16px;
}

.has-children {
  font-weight: 500;
}

.menu-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: rgb(25, 144, 255);
}

/* 添加基于菜单名称的选择方式 */
.menu-item[data-title="商品流通"],
.menu-item[data-title="流通指令"] {
  background: rgb(24, 144, 255);
}

.menu-item[data-title="商品流通"] span,
.menu-item[data-title="流通指令"] span {
  color: #fff;
}

.menu-arrow {
  margin-left: auto;
  font-size: 12px;
  transition: transform 0.3s;
}

.menu-arrow.expanded {
  transform: rotate(90deg);
}
</style>