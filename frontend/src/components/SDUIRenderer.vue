<template>
  <div class="sdui-renderer">
    <div v-if="error" class="sdui-error">
      <h3>渲染错误</h3>
      <p>{{ error }}</p>
    </div>
    
    <template v-else-if="rootComponents && rootComponents.length > 0">
      <component
        v-for="component in rootComponents"
        :key="component.id"
        :is="getComponentType(component.type)"
        v-bind="mapProps(component)"
        @action="handleAction"
      />
    </template>
    
    <div v-else class="sdui-empty">
      <p>无UI配置</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import componentMap from './sdui';
import { 
  UIComponent, 
  UIConfig, 
  ComponentActionEvent 
} from '../types/sdui';

// 定义组件属性
const props = defineProps<{
  config: UIConfig | any;
}>();

// 引入路由
const router = useRouter();

// 错误状态
const error = ref<string | null>(null);

// 获取根组件
const rootComponents = computed<UIComponent[]>(() => {
  try {
    // 检查配置格式
    if (!props.config) {
      return [];
    }
    
    // 兼容不同的API响应格式
    if (props.config.components) {
      return props.config.components;
    }
    
    if (props.config.screen && props.config.screen.components) {
      return props.config.screen.components;
    }
    
    return [];
  } catch (err) {
    error.value = `配置解析错误: ${err instanceof Error ? err.message : String(err)}`;
    return [];
  }
});

// 获取组件类型
const getComponentType = (type: string) => {
  if (!type) {
    console.warn('组件类型未定义');
    return 'div';
  }
  
  const component = componentMap[type];
  if (!component) {
    console.warn(`未知组件类型: ${type}`);
    return 'div';
  }
  
  return component;
};

// 映射组件属性
const mapProps = (component: UIComponent) => {
  return {
    id: component.id,
    style: component.style || {},
    properties: component.properties || {},
    events: component.events || {},
    children: component.children || [],
  };
};

// 处理动作
const handleAction = (action: ComponentActionEvent) => {
  console.log('组件动作:', action);
  
  // 处理导航
  if (action.type === 'navigation' && 'url' in action) {
    router.push(action.url as string);
    return;
  }
  
  // 处理其他类型的动作
  // TODO: 实现API调用等动作
};
</script>

<style scoped>
.sdui-renderer {
  width: 100%;
}

.sdui-error {
  color: #f56c6c;
  padding: 20px;
  border: 1px solid #f56c6c;
  border-radius: 4px;
  background-color: #fef0f0;
}

.sdui-empty {
  padding: 20px;
  text-align: center;
  color: #909399;
  border: 1px dashed #d3d3d3;
  border-radius: 4px;
}
</style> 