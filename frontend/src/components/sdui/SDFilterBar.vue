<template>
    <div class="sd-filter-bar">
        <div v-if="DEBUG" class="debug-info">
            <p>FilterBar Props: {{ JSON.stringify(props) }}</p>
        </div>
        <div class="filter-items">
            <div v-for="item in filterItems" :key="item.id" class="filter-item">
                <component :is="resolveComponent(item.type)" v-bind="item.props"
                    :value="getBindingValue(item.bindings?.value)"
                    @update:value="handleValueUpdate(item.bindings?.value, $event)" />
            </div>
        </div>
        <div class="filter-actions">
            <button v-for="action in filterActions" :key="action.text" :class="['filter-button', action.props?.type]"
                @click="handleAction(action.events?.click)">
                {{ action.text }}
            </button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import SDSelect from './SDSelect.vue';
import SDDatePicker from './SDDatePicker.vue';

// 调试模式
const DEBUG = ref(true);

const props = defineProps({
    id: {
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

const emit = defineEmits(['action', 'update:value']);

// 获取过滤项和操作按钮
const filterItems = computed(() => {
    console.log('Properties:', props.properties);
    return props.properties?.items || [];
});

const filterActions = computed(() => {
    return props.properties?.actions || [];
});

// 组件映射
const componentMap = {
    select: SDSelect,
    datePicker: SDDatePicker,
    dropdown: SDSelect,
    input: 'input'
};

// 组件挂载时检查配置
onMounted(() => {
    console.log('FilterBar mounted, props:', props);
    console.log('FilterBar items:', filterItems.value);
    console.log('FilterBar actions:', filterActions.value);
});

// 解析组件类型
const resolveComponent = (type: string) => {
    console.log('Resolving component type:', type);
    if (!type) return 'div';

    // 支持dropdown作为select的别名
    if (type.toLowerCase() === 'dropdown') {
        return SDSelect;
    }

    return componentMap[type as keyof typeof componentMap] || 'div';
};

// 获取绑定值
const getBindingValue = (binding: any) => {
    if (!binding) return null;
    // 这里应该根据binding.type和binding.source获取实际的值
    return '';
};

// 处理值更新
const handleValueUpdate = (binding: any, value: any) => {
    if (!binding) return;
    console.log('值更新:', binding, value);

    // 触发自定义事件通知父组件更新值
    emit('update:value', { id: binding.source, value });
};

// 处理动作
const handleAction = (event: any) => {
    if (!event) return;

    console.log('执行动作:', event);
    emit('action', {
        type: event?.type || 'click',
        target: event?.target || null,
        data: event?.data || null
    });
};
</script>

<style scoped>
.sd-filter-bar {
    background: #fff;
    padding: 16px;
    border: 1px solid #f0f0f0;
    margin-bottom: 8px;
}

.debug-info {
    margin-bottom: 10px;
    padding: 8px;
    background-color: #f8f8f8;
    border: 1px dashed #ccc;
    font-size: 12px;
    color: #666;
    white-space: pre-wrap;
    overflow: auto;
}

.filter-items {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 16px;
}

.filter-item {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.filter-item label {
    font-size: 14px;
    color: rgba(0, 0, 0, 0.85);
    line-height: 1.5715;
}

.filter-actions {
    display: flex;
    gap: 8px;
}

.filter-button {
    height: 32px;
    padding: 0 15px;
    border-radius: 2px;
    border: 1px solid #d9d9d9;
    background: #fff;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
    color: rgba(0, 0, 0, 0.65);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    line-height: 1.5715;
}

.filter-button.primary {
    background: rgb(24, 144, 255);
    border-color: rgb(24, 144, 255);
    color: #fff;
}

.filter-button:hover {
    color: #40a9ff;
    border-color: #40a9ff;
}

.filter-button.primary:hover {
    background: #40a9ff;
    border-color: #40a9ff;
    color: #fff;
}
</style>