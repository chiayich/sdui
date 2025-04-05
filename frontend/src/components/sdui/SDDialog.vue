<template>
    <div v-if="modelValue" class="sd-dialog__wrapper">
        <div class="sd-dialog__mask" @click="handleCancel"></div>
        <div class="sd-dialog" :style="{ width }">
            <div class="sd-dialog__header">
                <h3 class="sd-dialog__title">{{ title }}</h3>
                <button class="sd-dialog__close" @click="handleCancel">×</button>
            </div>

            <div class="sd-dialog__body">
                <slot></slot>
            </div>

            <div class="sd-dialog__footer">
                <slot name="footer">
                    <sd-button @click="handleCancel">取消</sd-button>
                    <sd-button type="primary" @click="handleConfirm">确定</sd-button>
                </slot>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import SDButton from './SDButton.vue';

interface Props {
    modelValue: boolean;
    title?: string;
    width?: string;
    closeOnClickMask?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
    title: '',
    width: '500px',
    closeOnClickMask: false,
});

const emit = defineEmits<{
    (e: 'update:modelValue', value: boolean): void;
    (e: 'confirm'): void;
    (e: 'cancel'): void;
}>();

const handleCancel = () => {
    emit('update:modelValue', false);
    emit('cancel');
};

const handleConfirm = () => {
    emit('confirm');
};
</script>

<style lang="scss" scoped>
.sd-dialog {
    &__wrapper {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 2000;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    &__mask {
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        background-color: rgba(0, 0, 0, 0.5);
        cursor: pointer;
    }

    &__close {
        position: absolute;
        top: 16px;
        right: 16px;
        padding: 0;
        background: transparent;
        border: none;
        font-size: 20px;
        line-height: 1;
        color: #909399;
        cursor: pointer;

        &:hover {
            color: #606266;
        }
    }

    & {
        position: relative;
        background: #fff;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        margin: 0 auto;
        max-height: calc(100vh - 100px);
        display: flex;
        flex-direction: column;
        min-width: 300px;
    }

    &__header {
        padding: 16px;
        border-bottom: 1px solid #dcdfe6;
        position: relative;
    }

    &__title {
        margin: 0;
        font-size: 16px;
        font-weight: 500;
        color: #303133;
        line-height: 24px;
    }

    &__body {
        padding: 16px;
        flex: 1;
        overflow-y: auto;
    }

    &__footer {
        padding: 16px;
        border-top: 1px solid #dcdfe6;
        display: flex;
        justify-content: flex-end;
        gap: 8px;
    }
}
</style>