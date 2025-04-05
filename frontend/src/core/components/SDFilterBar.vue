<template>
  <div class="sd-filter-bar">
    <div class="filter-items">
      <div v-for="item in props.items" :key="item.id" class="filter-item">
        <component
          :is="resolveComponent(item.type)"
          v-bind="item.props"
          :value="getBindingValue(item.bindings?.value)"
          @update:value="handleValueUpdate(item.bindings?.value, $event)"
        />
      </div>
    </div>
    <div class="filter-actions">
      <button
        v-for="action in props.actions"
        :key="action.text"
        :class="['filter-button', action.props?.type]"
        @click="handleAction(action.events?.click)"
      >
        {{ action.text }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SDSelect from './form/SDSelect.vue';
import SDDateRangePicker from './form/SDDateRangePicker.vue';
import SDDatePicker from './form/SDDatePicker.vue';

const props = defineProps<{
  items: any[];
  actions: any[];
}>();

const emit = defineEmits(['update:value']);

// 组件映射
const componentMap = {
  select: SDSelect,
  dateRangePicker: SDDateRangePicker,
  datePicker: SDDatePicker,
  input: 'input'
};

// 解析组件类型
const resolveComponent = (type: string) => {
  return componentMap[type as keyof typeof componentMap] || 'div';
};

// 获取绑定值
const getBindingValue = (binding: any) => {
  if (!binding) return null;
  // 这里应该根据binding.type和binding.source获取实际的值
  return '';
};

// 处理值更新
const handleValueUpdate = (binding: any, value: any) => {
  if (!binding) return;
  // 实际应用中这里会根据binding更新状态
  console.log('值更新:', binding, value);
  
  // 触发自定义事件通知父组件更新值
  emit('update:value', { id: binding.source, value });
};

// 处理动作
const handleAction = (actions: any[]) => {
  if (!actions) return;
  actions.forEach(action => {
    console.log('执行动作:', action);
  });
};
</script>

<style scoped>
.sd-filter-bar {
  background: #fff;
  padding: 16px;
  border: 1px solid #f0f0f0;
  margin-bottom: 8px;
}

.filter-items {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-item label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.85);
  line-height: 1.5715;
}

.filter-actions {
  display: flex;
  gap: 8px;
}

.filter-button {
  height: 32px;
  padding: 0 15px;
  border-radius: 2px;
  border: 1px solid #d9d9d9;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  color: rgba(0, 0, 0, 0.65);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1.5715;
}

.filter-button.primary {
  background: rgb(24, 144, 255);
  border-color: rgb(24, 144, 255);
  color: #fff;
}

.filter-button:hover {
  color: #40a9ff;
  border-color: #40a9ff;
}

.filter-button.primary:hover {
  background: #40a9ff;
  border-color: #40a9ff;
  color: #fff;
}
</style> 