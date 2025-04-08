<template>
    <component v-if="componentType" :is="componentType" :id="component.id" :style="component.style"
        :properties="componentProperties" :events="component.events" @action="handleAction">
        <!-- 递归渲染子组件 -->
        <template v-if="hasChildren">
            <component-renderer v-for="(child, index) in componentChildren" :key="`${component.id || 'comp'}-${index}`"
                :component="child" :context="context" @action="handleAction" />
        </template>
    </component>
    <div v-else class="unknown-component">
        未知组件类型: {{ component?.type || '未指定' }}
        <div class="debug-info">
            <p>可用组件: {{ availableComponents }}</p>
            <p>组件信息:</p>
            <pre>{{ JSON.stringify(component, null, 2) }}</pre>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue';
import componentMap from './index';

// 始终启用调试模式，方便排查
const DEBUG = ref(true);

const props = defineProps({
    component: {
        type: Object,
        required: true
    },
    context: {
        type: Object,
        default: () => ({})
    }
});

const emit = defineEmits(['action']);

// 检查组件的props属性，兼容处理传入的props
const componentProperties = computed(() => {
    // 优先使用component.properties
    if (props.component.properties) {
        return props.component.properties;
    }

    // 如果没有properties但有props，使用props
    if (props.component.props) {
        console.log(`组件${props.component.type}使用props替代properties:`, props.component.props);
        return props.component.props;
    }

    return {};
});

// 调试信息，打印组件数据
onMounted(() => {
    console.log('渲染组件:', props.component);
    console.log('组件类型:', props.component?.type);
    console.log('组件属性:', componentProperties.value);

    // 检查children和content字段
    if (props.component?.children) {
        console.log('组件children:', props.component.children);
    }

    if (props.component?.content) {
        console.log('组件content:', props.component.content);
        console.warn('注意: content字段将被用作children字段渲染');
    }
});

// 监听组件变化
watch(() => props.component, (newComp) => {
    console.log('组件更新:', newComp);
}, { deep: true });

// 获取组件子元素
const componentChildren = computed(() => {
    // 统一使用 children 字段
    if (Array.isArray(props.component.children) && props.component.children.length > 0) {
        console.log(`组件${props.component.type}包含${props.component.children.length}个子元素`);
        return props.component.children;
    }

    // 向后兼容：如果发现使用了其他字段，输出警告
    if (props.component.content) {
        console.warn(`组件${props.component.type}使用了已废弃的 content 字段，请使用 children 字段`);
        if (typeof props.component.content === 'object' && !Array.isArray(props.component.content)) {
            return [props.component.content];
        }
        if (Array.isArray(props.component.content)) {
            return props.component.content;
        }
    }

    if (props.component.components) {
        console.warn(`组件${props.component.type}使用了已废弃的 components 字段，请使用 children 字段`);
        if (Array.isArray(props.component.components)) {
            return props.component.components;
        }
    }

    console.log(`组件${props.component.type}没有子组件`);
    return [];
});

// 检查是否有子组件
const hasChildren = computed(() => {
    return componentChildren.value.length > 0;
});

// 获取组件类型
const componentType = computed(() => {
    if (!props.component || !props.component.type) {
        console.warn('组件缺少type属性:', props.component);
        return null;
    }

    // 获取组件类型
    const type = String(props.component.type).trim();
    console.log(`尝试解析组件类型: ${type}`);

    // 直接尝试精确匹配
    if (componentMap[type]) {
        console.log(`直接匹配组件: ${type} -> ${componentMap[type].name || '未命名组件'}`);
        return componentMap[type];
    }

    // 尝试小写匹配
    const typeLower = type.toLowerCase();
    if (componentMap[typeLower]) {
        console.log(`小写匹配组件: ${type} -> ${typeLower} -> ${componentMap[typeLower].name || '未命名组件'}`);
        return componentMap[typeLower];
    }

    // 尝试查找大小写不敏感的匹配
    const key = Object.keys(componentMap).find(
        k => k.toLowerCase() === typeLower
    );

    if (key) {
        console.log(`大小写不敏感匹配: ${type} -> ${key} -> ${componentMap[key].name || '未命名组件'}`);
        return componentMap[key];
    }

    // 尝试别名匹配 - dropdown 作为 select 的别名
    if (typeLower === 'dropdown') {
        console.log(`别名匹配: ${type} -> select`);
        return componentMap['select'];
    }

    // 输出详细的错误信息
    console.warn(`未找到组件类型: ${type}，可用组件:`, Object.keys(componentMap));
    return null;
});

// 获取可用组件列表
const availableComponents = computed(() => {
    return Object.keys(componentMap).join(', ');
});

// 处理组件动作
const handleAction = (action: any) => {
    console.log('组件动作:', action);
    emit('action', action);
};
</script>

<style scoped>
.unknown-component {
    padding: 12px;
    margin: 8px 0;
    border: 2px dashed #f56c6c;
    color: #f56c6c;
    background-color: #fef0f0;
    border-radius: 4px;
    font-weight: bold;
}

.debug-info {
    margin-top: 10px;
    font-size: 12px;
    color: #666;
    font-weight: normal;
    background-color: #f8f8f8;
    padding: 8px;
    border-radius: 4px;
    overflow: auto;
    max-height: 200px;
}

.debug-info pre {
    margin: 0;
    white-space: pre-wrap;
}
</style>