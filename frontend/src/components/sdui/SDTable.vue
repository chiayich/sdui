<template>
  <div class="sd-table">
    <table class="sd-table__content">
      <thead>
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
            :style="{ width: column.width }"
          >
            {{ column.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="row.id || index">
          <td v-for="column in columns" :key="column.key">
            <!-- 操作列 -->
            <template v-if="column.type === 'action'">
              <div class="sd-table__actions">
                <sd-button
                  v-for="action in column.actions"
                  :key="action.key"
                  :type="action.type || 'text'"
                  :disabled="action.disabled?.(row)"
                  @click="handleAction(action, row)"
                >
                  {{ action.text }}
                </sd-button>
              </div>
            </template>
            
            <!-- 自定义渲染 -->
            <template v-else-if="column.render">
              <component
                :is="column.render"
                :row="row"
                :column="column"
                :index="index"
              />
            </template>
            
            <!-- 默认渲染 -->
            <template v-else>
              {{ getValue(row, column.key) }}
            </template>
          </td>
        </tr>
        
        <!-- 空数据展示 -->
        <tr v-if="!data.length">
          <td :colspan="columns.length" class="sd-table__empty">
            {{ emptyText }}
          </td>
        </tr>
      </tbody>
    </table>
    
    <!-- 分页 -->
    <div v-if="showPagination" class="sd-table__pagination">
      <span class="sd-table__total">共 {{ total }} 条</span>
      <div class="sd-table__pages">
        <sd-button
          type="text"
          :disabled="currentPage <= 1"
          @click="handlePageChange(currentPage - 1)"
        >
          上一页
        </sd-button>
        <span class="sd-table__page-number">{{ currentPage }}</span>
        <sd-button
          type="text"
          :disabled="currentPage >= totalPages"
          @click="handlePageChange(currentPage + 1)"
        >
          下一页
        </sd-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import SDButton from './SDButton.vue';

interface TableColumn {
  key: string;
  title: string;
  width?: string;
  type?: 'action';
  actions?: Array<{
    key: string;
    text: string;
    type?: string;
    disabled?: (row: any) => boolean;
  }>;
  render?: any;
}

interface Props {
  columns: TableColumn[];
  data: any[];
  total?: number;
  currentPage?: number;
  pageSize?: number;
  showPagination?: boolean;
  emptyText?: string;
}

const props = withDefaults(defineProps<Props>(), {
  total: 0,
  currentPage: 1,
  pageSize: 10,
  showPagination: true,
  emptyText: '暂无数据',
});

const emit = defineEmits<{
  (e: 'action', action: string, row: any): void;
  (e: 'page-change', page: number): void;
}>();

const totalPages = computed(() => Math.ceil(props.total / props.pageSize));

const getValue = (row: any, key: string) => {
  return key.split('.').reduce((obj, key) => obj?.[key], row) ?? '';
};

const handleAction = (action: any, row: any) => {
  emit('action', action.key, row);
};

const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  emit('page-change', page);
};
</script>

<style lang="scss" scoped>
.sd-table {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  &__content {
    width: 100%;
    border-collapse: collapse;
    
    th, td {
      padding: 12px;
      text-align: left;
      font-size: 14px;
      border-bottom: 1px solid #ebeef5;
    }
    
    th {
      background-color: #f5f7fa;
      color: #909399;
      font-weight: 500;
    }
    
    td {
      color: #606266;
    }
  }
  
  &__actions {
    display: flex;
    gap: 8px;
  }
  
  &__empty {
    text-align: center;
    color: #909399;
    padding: 32px !important;
  }
  
  &__pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;
    border-top: 1px solid #ebeef5;
  }
  
  &__total {
    font-size: 14px;
    color: #606266;
  }
  
  &__pages {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  &__page-number {
    font-size: 14px;
    color: #606266;
  }
}
</style> 