<template>
    <component :is="titleTag" :class="['sd-title', className]" :style="computedStyle">
        <slot>{{ content }}</slot>
    </component>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
    /** 标题级别 (1-6) */
    level: {
        type: [Number, String],
        default: 1,
        validator: (value: number | string) => {
            const level = Number(value);
            return level >= 1 && level <= 6;
        }
    },
    /** 标题文本内容 */
    content: {
        type: String,
        default: ''
    },
    /** 字体大小 */
    fontSize: {
        type: [String, Number],
        default: null
    },
    /** 文本颜色 */
    color: {
        type: String,
        default: null
    },
    /** 文本对齐方式 */
    align: {
        type: String,
        default: null,
        validator: (value: string) => ['left', 'center', 'right'].includes(value)
    },
    /** 外边距 */
    margin: {
        type: String,
        default: null
    },
    /** 自定义类名 */
    className: {
        type: String,
        default: ''
    }
});

// 确定标题标签（h1-h6）
const titleTag = computed(() => {
    const level = Number(props.level);
    return `h${level}`;
});

// 计算样式
const computedStyle = computed(() => {
    const style: Record<string, string> = {};

    // 字体大小
    if (props.fontSize) {
        const fontSize = typeof props.fontSize === 'number'
            ? `${props.fontSize}px`
            : props.fontSize;
        style.fontSize = fontSize;
    }

    // 文本颜色
    if (props.color) {
        style.color = props.color;
    }

    // 对齐方式
    if (props.align) {
        style.textAlign = props.align;
    }

    // 外边距
    if (props.margin) {
        style.margin = props.margin;
    }

    return style;
});
</script>

<style scoped>
.sd-title {
    font-weight: 500;
    line-height: 1.5;
}

h1.sd-title {
    font-size: 2rem;
    margin: 1rem 0;
}

h2.sd-title {
    font-size: 1.75rem;
    margin: 0.875rem 0;
}

h3.sd-title {
    font-size: 1.5rem;
    margin: 0.75rem 0;
}

h4.sd-title {
    font-size: 1.25rem;
    margin: 0.625rem 0;
}

h5.sd-title {
    font-size: 1.125rem;
    margin: 0.5rem 0;
}

h6.sd-title {
    font-size: 1rem;
    margin: 0.5rem 0;
}
</style>