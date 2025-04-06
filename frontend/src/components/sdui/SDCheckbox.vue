<template>
  <div class="sd-checkbox" :style="style">
    <div class="checkbox-wrapper" :class="{ 'is-disabled': properties.disabled }">
      <label class="checkbox-label">
        <input
          type="checkbox"
          :id="id"
          :name="properties.name"
          :checked="isChecked"
          :disabled="properties.disabled"
          @change="handleChange"
        />
        <span class="checkbox-custom"></span>
        <span class="checkbox-text">
          {{ properties.label }}
          <span v-if="properties.required" class="required-mark">*</span>
        </span>
      </label>
    </div>
    <div v-if="hasError" class="error-message">{{ properties.errorMessage }}</div>
    <div v-if="properties.helpText" class="help-text">{{ properties.helpText }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

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
      value: false,
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

const checked = ref(props.properties.value || false);

const isChecked = computed(() => checked.value);
const hasError = computed(() => props.properties.hasError || false);

// 监听外部value变化
watch(() => props.properties.value, (newValue) => {
  checked.value = newValue;
}, { immediate: true });

const handleChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  checked.value = target.checked;
  
  emit('event', {
    type: 'change',
    componentId: props.id,
    value: checked.value,
    originalEvent: event
  });
};
</script>

<style scoped>
.sd-checkbox {
  margin-bottom: 16px;
  width: 100%;
}

.checkbox-wrapper {
  position: relative;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkbox-custom {
  position: relative;
  height: 16px;
  width: 16px;
  background-color: var(--bg-color, #fff);
  border: 1px solid var(--border-color, #d9d9d9);
  border-radius: 2px;
  transition: all 0.3s;
}

.checkbox-label:hover input ~ .checkbox-custom {
  border-color: var(--primary-color, #1890ff);
}

.checkbox-label input:checked ~ .checkbox-custom {
  background-color: var(--primary-color, #1890ff);
  border-color: var(--primary-color, #1890ff);
}

.checkbox-custom:after {
  content: "";
  position: absolute;
  display: none;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-label input:checked ~ .checkbox-custom:after {
  display: block;
}

.checkbox-text {
  margin-left: 8px;
  color: var(--text-color, #333);
}

.required-mark {
  color: var(--error-color, #ff4d4f);
  margin-left: 4px;
}

.is-disabled .checkbox-label {
  cursor: not-allowed;
  color: var(--disabled-text, #bfbfbf);
}

.is-disabled .checkbox-custom {
  background-color: var(--disabled-bg, #f5f5f5);
  border-color: var(--border-color, #d9d9d9);
}

.is-disabled .checkbox-label input:checked ~ .checkbox-custom {
  background-color: var(--disabled-primary, #d9d9d9);
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