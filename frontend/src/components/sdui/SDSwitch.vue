<template>
  <div class="sd-switch" :style="style">
    <div class="switch-container">
      <span v-if="properties.labelPosition === 'left'" class="switch-label">
        {{ properties.label }}
        <span v-if="properties.required" class="required-mark">*</span>
      </span>
      
      <button
        :id="id"
        type="button"
        role="switch"
        class="switch"
        :class="{
          'is-checked': isChecked,
          'is-disabled': properties.disabled,
          'is-small': properties.size === 'small',
          'is-large': properties.size === 'large'
        }"
        :aria-checked="isChecked"
        :disabled="properties.disabled"
        @click="toggle"
      >
        <span class="switch-core">
          <span class="switch-thumb"></span>
        </span>
        <span v-if="properties.loading" class="switch-loading"></span>
      </button>
      
      <span v-if="properties.labelPosition !== 'left'" class="switch-label">
        {{ properties.label }}
        <span v-if="properties.required" class="required-mark">*</span>
      </span>
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
      value: false,
      labelPosition: 'right',
      size: 'default',
      loading: false,
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

const toggle = () => {
  if (props.properties.disabled || props.properties.loading) {
    return;
  }
  
  checked.value = !checked.value;
  
  emit('event', {
    type: 'change',
    componentId: props.id,
    value: checked.value
  });
};
</script>

<style scoped>
.sd-switch {
  margin-bottom: 16px;
  width: 100%;
}

.switch-container {
  display: flex;
  align-items: center;
}

.switch-label {
  margin-right: 8px;
  color: var(--text-color, #333);
}

.switch-container .switch-label:last-child {
  margin-right: 0;
  margin-left: 8px;
}

.required-mark {
  color: var(--error-color, #ff4d4f);
  margin-left: 4px;
}

.switch {
  position: relative;
  display: inline-flex;
  align-items: center;
  width: 40px;
  height: 20px;
  box-sizing: border-box;
  border: 0;
  outline: none;
  background: var(--disabled-bg, #ccc);
  border-radius: 10px;
  transition: all 0.3s;
  cursor: pointer;
  padding: 0;
}

.switch.is-checked {
  background-color: var(--primary-color, #1890ff);
}

.switch.is-disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.switch.is-small {
  width: 28px;
  height: 16px;
}

.switch.is-large {
  width: 52px;
  height: 26px;
}

.switch-core {
  width: 100%;
  height: 100%;
  position: relative;
  display: inline-block;
}

.switch-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #fff;
  transition: all 0.3s;
  box-shadow: 0 2px 4px 0 rgba(0, 35, 11, 0.2);
}

.switch.is-checked .switch-thumb {
  left: calc(100% - 18px);
}

.switch.is-small .switch-thumb {
  width: 12px;
  height: 12px;
}

.switch.is-small.is-checked .switch-thumb {
  left: calc(100% - 14px);
}

.switch.is-large .switch-thumb {
  width: 22px;
  height: 22px;
}

.switch.is-large.is-checked .switch-thumb {
  left: calc(100% - 24px);
}

.switch-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  border: 1px solid transparent;
  border-top-color: var(--primary-color, #1890ff);
  border-right-color: var(--primary-color, #1890ff);
  animation: switch-loading 1s infinite linear;
}

@keyframes switch-loading {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
  }
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