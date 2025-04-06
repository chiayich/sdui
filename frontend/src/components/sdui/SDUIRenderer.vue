<template>
  <div class="sdui-renderer" :class="rootClass">
    <div v-if="loading" class="sdui-loading">
      <slot name="loading">
        <div class="loading-spinner"></div>
      </slot>
    </div>
    <div v-else-if="error" class="sdui-error">
      <slot name="error" :error="error">
        <div class="error-message">{{ error }}</div>
      </slot>
    </div>
    <template v-else>
      <!-- 渲染页面内容 -->
      <template v-if="config && config.type === 'page'">
        <h1 v-if="config.title" class="page-title">{{ config.title }}</h1>
        <component-renderer v-if="config.layout" :component="config.layout" :context="context" @action="handleAction" />
        <component-renderer v-else-if="config.content" v-for="(component, index) in config.content"
          :key="`root-${index}`" :component="component" :context="context" @action="handleAction" />
      </template>
      <!-- 渲染单个组件 -->
      <template v-else-if="config">
        <component-renderer :component="config" :context="context" @action="handleAction" />
      </template>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ComponentRenderer from './ComponentRenderer.vue';

const props = defineProps({
  // 直接传入配置对象
  config: {
    type: Object,
    default: null
  },
  // 或者传入API路径获取配置
  schema: {
    type: String,
    default: ''
  },
  // 仅加载特定的组件IDs
  componentIds: {
    type: Array,
    default: () => []
  },
  // 是否加载子组件
  includeChildren: {
    type: Boolean,
    default: true
  },
  // 是否加载数据部分
  includeData: {
    type: Boolean,
    default: true
  },
  // 根元素CSS类名
  rootClass: {
    type: String,
    default: ''
  },
  // 初始上下文数据
  initialContext: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['loaded', 'error', 'action']);
const router = useRouter();

const loading = ref(false);
const error = ref(null);
const configData = ref(props.config);
const context = reactive({
  ...props.initialContext
});

// 添加配置调试日志
const config = computed(() => {
  console.log('当前配置数据:', configData.value);
  return configData.value;
});

// 加载配置
const loadConfig = async () => {
  if (!props.schema) return;

  loading.value = true;
  error.value = null;

  try {
    // 构建请求参数
    const params = {};
    if (props.componentIds && props.componentIds.length > 0) {
      params.component_ids = props.componentIds;
    }
    if (props.includeChildren !== undefined) {
      params.include_children = props.includeChildren;
    }
    if (props.includeData !== undefined) {
      params.include_data = props.includeData;
    }

    console.log('加载UI配置，URL:', props.schema, '参数:', params);
    const response = await axios.get(props.schema, { params });
    console.log('获取UI配置成功:', response.data);
    configData.value = response.data;
    emit('loaded', configData.value);
  } catch (err) {
    console.error('Failed to load UI schema:', err);
    error.value = err.response?.data?.detail || 'Failed to load UI configuration';
    emit('error', error.value);
  } finally {
    loading.value = false;
  }
};

// 处理组件动作
const handleAction = (action) => {
  console.log('Action received:', action);
  emit('action', action);

  // 处理导航动作
  if (action.type === 'navigate' && action.target) {
    router.push(action.target);
  }

  // 处理状态更新动作
  if (action.type === 'updateState' && action.key) {
    context[action.key] = action.value;
  }

  // 处理API调用动作
  if (action.type === 'apiCall' && action.endpoint) {
    // 实现API调用逻辑
  }
};

// 监听schema变化时重新加载配置
watch(() => props.schema, () => {
  if (props.schema) {
    loadConfig();
  }
});

// 监听直接传入的config变化
watch(() => props.config, (newConfig) => {
  if (newConfig) {
    configData.value = newConfig;
  }
});

// 当组件挂载时加载配置
onMounted(() => {
  if (props.schema) {
    loadConfig();
  }
});
</script>

<style scoped>
.sdui-renderer {
  width: 100%;
}

.sdui-loading {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.sdui-error {
  padding: 20px;
  color: #e74c3c;
  text-align: center;
}

.page-title {
  margin-bottom: 20px;
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