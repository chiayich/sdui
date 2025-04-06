<template>
    <i :class="iconClass" :style="computedStyle"></i>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
    /** 图标名称 */
    name: {
        type: String,
        required: true
    },
    /** 图标大小 */
    size: {
        type: [String, Number],
        default: 'inherit'
    },
    /** 图标颜色 */
    color: {
        type: String,
        default: 'inherit'
    },
    /** 自定义样式类 */
    className: {
        type: String,
        default: ''
    }
});

// 计算图标样式类
const iconClass = computed(() => {
    // 默认使用Element Plus图标
    const baseClass = `el-icon-${props.name}`;
    return props.className ? `${baseClass} ${props.className}` : baseClass;
});

// 计算样式
const computedStyle = computed(() => {
    const style: Record<string, string> = {};

    // 处理大小
    if (props.size !== 'inherit') {
        const size = typeof props.size === 'number' ? `${props.size}px` : props.size;
        style.fontSize = size;
    }

    // 处理颜色
    if (props.color !== 'inherit') {
        style.color = props.color;
    }

    return style;
});
</script>

<style scoped>
i {
    display: inline-flex;
    justify-content: center;
    align-items: center;
}
</style>