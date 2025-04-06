<template>
    <div class="sd-date-picker">
        <label v-if="properties.label" class="sd-date-picker-label">
            {{ properties.label }}
            <span v-if="properties.required" class="required-mark">*</span>
        </label>
        <input type="date" :value="modelValue" class="sd-date-input" :placeholder="properties.placeholder || '请选择日期'"
            :disabled="properties.disabled" @input="handleInput" @change="handleChange" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps({
    id: {
        type: String,
        default: ''
    },
    value: {
        type: String,
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

const modelValue = ref(props.value || props.properties?.value || '');

const handleInput = (e: Event) => {
    const target = e.target as HTMLInputElement;
    modelValue.value = target.value;
};

const handleChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    emit('update:value', target.value);

    if (props.events?.change) {
        emit('action', {
            type: 'change',
            data: target.value
        });
    }
};
</script>

<style scoped>
.sd-date-picker {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.sd-date-picker-label {
    font-size: 14px;
    color: rgba(0, 0, 0, 0.85);
}

.required-mark {
    color: #ff4d4f;
    margin-left: 4px;
}

.sd-date-input {
    width: 100%;
    height: 32px;
    padding: 4px 11px;
    color: rgba(0, 0, 0, 0.85);
    font-size: 14px;
    background-color: #fff;
    border: 1px solid #d9d9d9;
    border-radius: 2px;
    transition: all 0.3s;
}

.sd-date-input:hover {
    border-color: #40a9ff;
}

.sd-date-input:focus {
    border-color: #40a9ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
    outline: none;
}

.sd-date-input:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
    color: rgba(0, 0, 0, 0.25);
}
</style>
