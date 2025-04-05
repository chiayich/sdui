<template>
    <form class="sd-form" @submit.prevent="handleSubmit">
        <div v-for="field in fields" :key="field.key" class="sd-form__field" :class="{ 'is-required': field.required }">
            <label :for="field.key" class="sd-form__label">
                {{ field.label }}
                <span v-if="field.required" class="sd-form__required">*</span>
            </label>

            <div class="sd-form__content">
                <!-- 文本输入 -->
                <input v-if="field.type === 'text'" :id="field.key" v-model="formData[field.key]" type="text"
                    class="sd-form__input" :placeholder="field.placeholder" />

                <!-- 数字输入 -->
                <input v-else-if="field.type === 'number'" :id="field.key" v-model.number="formData[field.key]"
                    type="number" class="sd-form__input" :min="field.min" :max="field.max" :step="field.step" />

                <!-- 选择框 -->
                <select v-else-if="field.type === 'select'" :id="field.key" v-model="formData[field.key]"
                    class="sd-form__select">
                    <option value="">{{ field.placeholder || '请选择' }}</option>
                    <option v-for="option in field.options" :key="option.value" :value="option.value">
                        {{ option.label }}
                    </option>
                </select>

                <!-- 日期选择 -->
                <input v-else-if="field.type === 'date'" :id="field.key" v-model="formData[field.key]" type="date"
                    class="sd-form__input" />

                <!-- 文本域 -->
                <textarea v-else-if="field.type === 'textarea'" :id="field.key" v-model="formData[field.key]"
                    class="sd-form__textarea" :placeholder="field.placeholder" :rows="field.rows || 3"></textarea>

                <!-- 单选框组 -->
                <div v-else-if="field.type === 'radio'" class="sd-form__radio-group">
                    <label v-for="option in field.options" :key="option.value" class="sd-form__radio">
                        <input type="radio" :name="field.key" :value="option.value" v-model="formData[field.key]" />
                        <span>{{ option.label }}</span>
                    </label>
                </div>

                <!-- 复选框组 -->
                <div v-else-if="field.type === 'checkbox'" class="sd-form__checkbox-group">
                    <label v-for="option in field.options" :key="option.value" class="sd-form__checkbox">
                        <input type="checkbox" :value="option.value" v-model="formData[field.key]" />
                        <span>{{ option.label }}</span>
                    </label>
                </div>

                <div v-if="errors[field.key]" class="sd-form__error">
                    {{ errors[field.key] }}
                </div>
            </div>
        </div>
    </form>
</template>

<script lang="ts" setup>
import { reactive, ref, watch } from 'vue';

interface FormField {
    key: string;
    label: string;
    type: 'text' | 'number' | 'select' | 'date' | 'textarea' | 'radio' | 'checkbox';
    required?: boolean;
    placeholder?: string;
    options?: Array<{ label: string; value: any }>;
    min?: number;
    max?: number;
    step?: number;
    rows?: number;
    validator?: (value: any) => string | undefined;
}

interface Props {
    fields: FormField[];
    modelValue?: Record<string, any>;
}

const props = withDefaults(defineProps<Props>(), {
    modelValue: () => ({}),
});

const emit = defineEmits<{
    (e: 'update:modelValue', value: Record<string, any>): void;
    (e: 'validate', valid: boolean): void;
}>();

const formData = reactive<Record<string, any>>({});
const errors = ref<Record<string, string>>({});

// 初始化表单数据
const initFormData = () => {
    Object.assign(formData, props.modelValue);
};

// 监听 modelValue 变化
watch(() => props.modelValue, (newValue) => {
    initFormData();
}, { deep: true });

// 监听表单数据变化
watch(formData, (newValue) => {
    emit('update:modelValue', { ...newValue });
}, { deep: true });

// 表单验证
const validate = () => {
    let isValid = true;
    errors.value = {};

    for (const field of props.fields) {
        const value = formData[field.key];

        // 必填验证
        if (field.required) {
            if (value === undefined || value === null || value === '') {
                errors.value[field.key] = `${field.label}不能为空`;
                isValid = false;
                continue;
            }

            if (typeof value === 'string' && value.trim() === '') {
                errors.value[field.key] = `${field.label}不能为空`;
                isValid = false;
                continue;
            }
        }

        // 自定义验证
        if (field.validator && value !== undefined && value !== null) {
            const error = field.validator(value);
            if (error) {
                errors.value[field.key] = error;
                isValid = false;
            }
        }
    }

    emit('validate', isValid);
    return isValid;
};

// 重置表单
const reset = () => {
    Object.keys(formData).forEach(key => {
        formData[key] = '';
    });
    errors.value = {};
};

// 处理表单提交
const handleSubmit = (e: Event) => {
    e.preventDefault();
    validate();
};

// 初始化
initFormData();

// 暴露方法
defineExpose({
    validate,
    reset,
    formData,
});
</script>

<style lang="scss" scoped>
.sd-form {
    &__field {
        margin-bottom: 20px;

        &.is-required .sd-form__label {
            font-weight: 500;
        }
    }

    &__label {
        display: block;
        margin-bottom: 8px;
        font-size: 14px;
        color: #606266;
    }

    &__required {
        color: #f56c6c;
        margin-left: 4px;
    }

    &__content {
        position: relative;
    }

    &__input,
    &__select,
    &__textarea {
        width: 100%;
        padding: 0 12px;
        border: 1px solid #dcdfe6;
        border-radius: 4px;
        font-size: 14px;
        color: #606266;
        transition: border-color 0.3s;
        box-sizing: border-box;

        &:focus {
            outline: none;
            border-color: var(--primary-color, #1890ff);
        }

        &::placeholder {
            color: #c0c4cc;
        }
    }

    &__input,
    &__select {
        height: 32px;
    }

    &__textarea {
        padding: 8px 12px;
        resize: vertical;
    }

    &__radio-group,
    &__checkbox-group {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }

    &__radio,
    &__checkbox {
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        font-size: 14px;
        color: #606266;

        input {
            margin: 0;
        }
    }

    &__error {
        position: absolute;
        font-size: 12px;
        color: #f56c6c;
        margin-top: 4px;
    }
}
</style>