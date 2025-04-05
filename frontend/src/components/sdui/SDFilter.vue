<template>
  <div class="sd-filter">
    <div class="sd-filter__form">
      <div
        v-for="field in fields"
        :key="field.key"
        class="sd-filter__field"
      >
        <label :for="field.key" class="sd-filter__label">{{ field.label }}</label>
        
        <!-- 输入框 -->
        <input
          v-if="field.type === 'text'"
          :id="field.key"
          v-model="formData[field.key]"
          type="text"
          class="sd-filter__input"
          :placeholder="field.placeholder"
        />
        
        <!-- 选择框 -->
        <select
          v-else-if="field.type === 'select'"
          :id="field.key"
          v-model="formData[field.key]"
          class="sd-filter__select"
        >
          <option value="">{{ field.placeholder || '请选择' }}</option>
          <option
            v-for="option in field.options"
            :key="option.value"
            :value="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        
        <!-- 日期选择 -->
        <input
          v-else-if="field.type === 'date'"
          :id="field.key"
          v-model="formData[field.key]"
          type="date"
          class="sd-filter__input"
        />
        
        <!-- 数字输入 -->
        <input
          v-else-if="field.type === 'number'"
          :id="field.key"
          v-model.number="formData[field.key]"
          type="number"
          class="sd-filter__input"
          :min="field.min"
          :max="field.max"
          :step="field.step"
        />
      </div>
      
      <div class="sd-filter__actions">
        <sd-button type="primary" @click="handleSearch">查询</sd-button>
        <sd-button type="info" @click="handleReset">重置</sd-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import SDButton from './SDButton.vue';

interface FilterField {
  key: string;
  label: string;
  type: 'text' | 'select' | 'date' | 'number';
  placeholder?: string;
  options?: Array<{ label: string; value: any }>;
  min?: number;
  max?: number;
  step?: number;
}

interface Props {
  fields: FilterField[];
}

const props = defineProps<Props>();
const emit = defineEmits<{
  (e: 'search', formData: Record<string, any>): void;
  (e: 'reset'): void;
}>();

const formData = reactive<Record<string, any>>({});

// 初始化表单数据
for (const field of props.fields) {
  formData[field.key] = '';
}

const handleSearch = () => {
  emit('search', { ...formData });
};

const handleReset = () => {
  for (const key in formData) {
    formData[key] = '';
  }
  emit('reset');
};
</script>

<style lang="scss" scoped>
.sd-filter {
  padding: 16px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  &__form {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
  }
  
  &__field {
    display: flex;
    flex-direction: column;
    min-width: 200px;
  }
  
  &__label {
    margin-bottom: 8px;
    font-size: 14px;
    color: #606266;
  }
  
  &__input,
  &__select {
    height: 32px;
    padding: 0 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    font-size: 14px;
    color: #606266;
    transition: border-color 0.3s;
    
    &:focus {
      outline: none;
      border-color: var(--primary-color, #1890ff);
    }
    
    &::placeholder {
      color: #c0c4cc;
    }
  }
  
  &__actions {
    display: flex;
    align-items: flex-end;
    gap: 8px;
  }
}
</style> 