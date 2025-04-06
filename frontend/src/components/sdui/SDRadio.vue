<template>
  <div class="sd-radio" :style="style">
    <div v-if="properties.label" class="radio-group-label">
      {{ properties.label }}
      <span v-if="properties.required" class="required-mark">*</span>
    </div>
    <div class="radio-group" :class="{ 'is-vertical': properties.vertical }">
      <div
        v-for="option in properties.options"
        :key="option.value"
        class="radio-wrapper"
        :class="{ 'is-disabled': properties.disabled || option.disabled }"
      >
        <label class="radio-label">
          <input
            type="radio"
            :id="`${id}-${option.value}`"
            :name="properties.name || id"
            :value="option.value"
            :checked="selectedValue === option.value"
            :disabled="properties.disabled || option.disabled"
            @change="handleChange(option.value)"
          />
          <span class="radio-custom"></span>
          <span class="radio-text">{{ option.label }}</span>
        </label>
      </div>
    </div>
    <div v-if="hasError" class="error-message">{{ properties.errorMessage }}</div>
    <div v-if="properties.helpText" class="help-text">{{ properties.helpText }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  properties: {
    type: Object,
    required: true,
    default: () => ({
      name: '',
      label: '',
      options: [],
      value: undefined,
      vertical: false,
      disabled: false,
      required: false,
      errorMessage: '',
      hasError: false,
      helpText: ''
    })
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

const emit = defineEmits(['event']);

const selectedValue = ref(props.properties.value);

const hasError = computed(() => props.properties.hasError || false);

// 监听外部value变化
watch(() => props.properties.value, (newValue) => {
  selectedValue.value = newValue;
}, { immediate: true });

const handleChange = (value: string | number) => {
  selectedValue.value = value;
  
  emit('event', {
    type: 'change',
    componentId: props.id,
    value: selectedValue.value
  });
};
</script>

<style scoped>
.sd-radio {
  margin-bottom: 16px;
  width: 100%;
}

.radio-group-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--text-color, #333);
}

.required-mark {
  color: var(--error-color, #ff4d4f);
  margin-left: 4px;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.radio-group.is-vertical {
  flex-direction: column;
  gap: 8px;
}

.radio-wrapper {
  position: relative;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.radio-label input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.radio-custom {
  position: relative;
  height: 16px;
  width: 16px;
  background-color: var(--bg-color, #fff);
  border: 1px solid var(--border-color, #d9d9d9);
  border-radius: 50%;
  transition: all 0.3s;
}

.radio-label:hover input ~ .radio-custom {
  border-color: var(--primary-color, #1890ff);
}

.radio-label input:checked ~ .radio-custom {
  border-color: var(--primary-color, #1890ff);
  border-width: 5px;
  background-color: white;
}

.radio-text {
  margin-left: 8px;
  color: var(--text-color, #333);
}

.is-disabled .radio-label {
  cursor: not-allowed;
  color: var(--disabled-text, #bfbfbf);
}

.is-disabled .radio-custom {
  background-color: var(--disabled-bg, #f5f5f5);
  border-color: var(--border-color, #d9d9d9);
}

.is-disabled .radio-label input:checked ~ .radio-custom {
  border-color: var(--disabled-primary, #d9d9d9);
}

.error-message {
  color: var(--error-color, #ff4d4f);
  font-size: 12px;
  margin-top: 4px;
}

.help-text {
  color: var(--text-light, #999);
  font-size: 12px;
  margin-top: 4px;
}
</style> 