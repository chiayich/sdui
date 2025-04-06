<template>
  <div class="sd-select" :style="style">
    <div v-if="DEBUG" class="debug-info">
      <p>Select Props: {{ JSON.stringify(props) }}</p>
    </div>
    <label v-if="properties.label" class="sd-select-label">
      {{ properties.label }}
      <span v-if="properties.required" class="required-mark">*</span>
    </label>
    <div class="select-wrapper" :class="{ 'is-error': hasError, 'is-disabled': properties.disabled }">
      <select :id="id" v-model="selectedValue" :name="properties.name" :disabled="properties.disabled"
        :multiple="properties.multiple" @change="handleChange" @focus="handleFocus" @blur="handleBlur">
        <option v-if="properties.placeholder" value="" disabled>
          {{ properties.placeholder }}
        </option>
        <option v-for="option in options" :key="option.value" :value="option.value" :disabled="option.disabled">
          {{ option.label }}
        </option>
      </select>
      <div class="select-arrow" v-if="!properties.multiple">
        <svg xmlns="http://www.w3.org/2000/svg" width="10" height="6" viewBox="0 0 10 6" fill="none">
          <path d="M1 1L5 5L9 1" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
            stroke-linejoin="round" />
        </svg>
      </div>
    </div>
    <div v-if="hasError" class="error-message">{{ properties.errorMessage }}</div>
    <div v-if="properties.helpText" class="help-text">{{ properties.helpText }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue';

// 调试模式
const DEBUG = ref(true);

const props = defineProps({
  id: {
    type: String,
    default: ''
  },
  value: {
    type: [String, Number, Array],
    default: ''
  },
  properties: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  },
  style: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['update:value', 'action']);

// 组件挂载时检查配置
onMounted(() => {
  console.log('Select mounted, props:', props);
  console.log('Select options:', options.value);
});

// 选项列表
const options = computed(() => {
  return props.properties?.options || [];
});

// 选中值
const selectedValue = ref(props.value || props.properties?.defaultValue || '');

// 是否有错误
const hasError = computed(() => {
  return Boolean(props.properties?.errorMessage);
});

// 监听value变化
watch(() => props.value, (newValue) => {
  selectedValue.value = newValue;
});

// 处理变更事件
const handleChange = (e: Event) => {
  const target = e.target as HTMLSelectElement;
  emit('update:value', target.value);

  // 触发action事件
  if (props.events?.change) {
    emit('action', {
      type: 'change',
      value: target.value
    });
  }
};

// 处理聚焦事件
const handleFocus = () => {
  if (props.events?.focus) {
    emit('action', {
      type: 'focus'
    });
  }
};

// 处理失焦事件
const handleBlur = () => {
  if (props.events?.blur) {
    emit('action', {
      type: 'blur'
    });
  }
};
</script>

<style scoped>
.sd-select {
  display: flex;
  flex-direction: column;
  gap: 4px;
  width: 100%;
}

.debug-info {
  margin-bottom: 10px;
  padding: 8px;
  background-color: #f8f8f8;
  border: 1px dashed #ccc;
  font-size: 12px;
  color: #666;
  white-space: pre-wrap;
  overflow: auto;
}

.sd-select-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.85);
  margin-bottom: 4px;
}

.required-mark {
  color: #ff4d4f;
  margin-left: 4px;
}

.select-wrapper {
  position: relative;
  width: 100%;
}

select {
  appearance: none;
  width: 100%;
  height: 32px;
  padding: 4px 11px;
  padding-right: 30px;
  color: rgba(0, 0, 0, 0.85);
  font-size: 14px;
  background-color: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  transition: all 0.3s;
}

select:hover {
  border-color: #40a9ff;
}

select:focus {
  border-color: #40a9ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.select-arrow {
  position: absolute;
  top: 50%;
  right: 11px;
  transform: translateY(-50%);
  pointer-events: none;
  color: rgba(0, 0, 0, 0.25);
}

.is-disabled select {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: rgba(0, 0, 0, 0.25);
}

.is-error select {
  border-color: #ff4d4f;
}

.error-message {
  color: #ff4d4f;
  font-size: 14px;
  line-height: 1.5;
}

.help-text {
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
  line-height: 1.5;
}
</style>