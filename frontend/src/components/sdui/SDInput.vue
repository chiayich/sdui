<template>
  <div class="sd-input" :style="style">
    <label v-if="properties.label" :for="id">{{ properties.label }}</label>
    <input
      :id="id"
      :type="properties.type || 'text'"
      :value="modelValue"
      @input="updateValue"
      :placeholder="properties.placeholder || ''"
      :disabled="properties.disabled"
      :readonly="properties.readonly"
      :maxlength="properties.maxLength"
      :class="{ 'error': properties.error }"
    />
    <small v-if="properties.helpText" class="help-text">{{ properties.helpText }}</small>
    <small v-if="properties.error" class="error-text">{{ properties.error }}</small>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

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
  modelValue: {
    type: [String, Number],
    default: ''
  },
  events: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['update:modelValue', 'action']);

const updateValue = (event: Event) => {
  const value = (event.target as HTMLInputElement).value;
  emit('update:modelValue', value);
  
  if (props.properties.onChange) {
    emit('action', {
      type: 'input',
      componentId: props.id,
      value,
      event: props.properties.onChange
    });
  }
};
</script>

<style scoped>
.sd-input {
  margin-bottom: 16px;
  width: 100%;
}

.sd-input label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.sd-input input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
  line-height: 1.5;
}

.sd-input input:focus {
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.sd-input input:hover {
  border-color: #c0c4cc;
}

.sd-input input:disabled {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
  color: #c0c4cc;
  cursor: not-allowed;
}

.sd-input input.error {
  border-color: #f56c6c;
}

.sd-input .help-text {
  display: block;
  margin-top: 4px;
  color: #909399;
  font-size: 12px;
}

.sd-input .error-text {
  display: block;
  margin-top: 4px;
  color: #f56c6c;
  font-size: 12px;
}
</style> 