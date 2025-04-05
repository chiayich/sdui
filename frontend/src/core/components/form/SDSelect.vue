<template>
  <div class="sd-select" :style="style">
    <div class="select-container" @click="toggleDropdown">
      <input 
        type="text" 
        class="select-input" 
        :placeholder="placeholder || '请选择'" 
        readonly 
        :value="displayValue"
      />
      <div class="select-arrow" :class="{ 'active': isOpen }">▼</div>
    </div>
    
    <div v-if="isOpen" class="select-dropdown">
      <div 
        v-for="option in options" 
        :key="option.value" 
        class="select-option"
        :class="{ 'selected': value === option.value }"
        @click.stop="handleSelect(option)"
      >
        {{ option.label }}
      </div>
      
      <div class="select-footer">
        <button class="select-all" @click.stop="handleSelectAll">全选</button>
        <button class="select-clear" @click.stop="handleClear">清空</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

interface SelectOption {
  value: string;
  label: string;
}

// 定义组件属性
interface Props {
  placeholder?: string;
  style?: Record<string, string>;
  value?: string;
  options?: SelectOption[];
  defaultValue?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:value']);

// 下拉框状态
const isOpen = ref(false);
const selectedValue = ref(props.value || props.defaultValue || '');

// 显示的文本值
const displayValue = computed(() => {
  if (!selectedValue.value || !props.options) return '';
  const option = props.options.find(opt => opt.value === selectedValue.value);
  return option ? option.label : '';
});

// 切换下拉框
const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

// 选择选项
const handleSelect = (option: SelectOption) => {
  selectedValue.value = option.value;
  emit('update:value', option.value);
  isOpen.value = false;
};

// 全选功能
const handleSelectAll = () => {
  // 这里实际应用中可能是多选，现在仅演示
  if (props.options && props.options.length > 0) {
    // 简单实现：选择第一个选项
    const firstOption = props.options[0];
    selectedValue.value = firstOption.value;
    emit('update:value', firstOption.value);
  }
  isOpen.value = false;
};

// 清空选择
const handleClear = () => {
  selectedValue.value = '';
  emit('update:value', '');
  isOpen.value = false;
};

// 点击外部关闭下拉框
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.sd-select')) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  // 如果有默认值但没有设置value，则触发一次更新
  if (!props.value && props.defaultValue) {
    emit('update:value', props.defaultValue);
  }
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.sd-select {
  position: relative;
  width: 100%;
  min-width: 120px;
}

.select-container {
  position: relative;
  width: 100%;
}

.select-input {
  width: 100%;
  padding: 4px 30px 4px 11px;
  height: 32px;
  line-height: 1.5;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  cursor: pointer;
  background-color: #fff;
}

.select-input:hover {
  border-color: #40a9ff;
}

.select-arrow {
  position: absolute;
  right: 11px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #666;
  pointer-events: none;
  transition: transform 0.3s;
}

.select-arrow.active {
  transform: translateY(-50%) rotate(180deg);
}

.select-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  max-height: 200px;
  overflow-y: auto;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  margin-top: 4px;
}

.select-option {
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.3s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.select-option:hover {
  background: #f5f5f5;
}

.select-option.selected {
  background-color: #e6f7ff;
  color: #1890ff;
  font-weight: 500;
}

.select-footer {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-top: 1px solid #f0f0f0;
}

.select-all, .select-clear {
  background: none;
  border: none;
  cursor: pointer;
  color: #1890ff;
  padding: 0;
  font-size: 14px;
}

.select-all:hover, .select-clear:hover {
  color: #40a9ff;
}
</style> 