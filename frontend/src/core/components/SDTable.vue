<template>
  <div class="sd-table">
    <table>
      <thead>
        <tr>
          <th v-for="column in props.columns" :key="column.dataIndex" :style="{ width: column.width + 'px' }">
            {{ column.title }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in tableData" :key="index">
          <td 
            v-for="column in props.columns" 
            :key="column.dataIndex"
            :class="[column.align ? `text-${column.align}` : '', column.className]"
          >
            {{ getCellValue(row, column) }}
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="props.pagination" class="table-pagination">
      <div class="pagination-info" v-if="props.pagination.showTotal">
        共 {{ total }} 条
      </div>
      <div class="pagination-buttons">
        <button
          :disabled="currentPage === 1"
          @click="handlePageChange(currentPage - 1)"
        >
          上一页
        </button>
        <span class="page-number">{{ currentPage }}</span>
        <button
          :disabled="currentPage * pageSize >= total"
          @click="handlePageChange(currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface TableColumn {
  title: string;
  dataIndex: string;
  width?: number;
  align?: 'left' | 'center' | 'right';
  className?: string;
}

interface TablePagination {
  pageSize: number;
  showTotal?: boolean;
}

interface TableBinding {
  dataSource?: {
    type: string;
    source: string;
  };
}

interface TableProps {
  columns: TableColumn[];
  dataSource?: Record<string, any>[];
  pagination?: TablePagination;
  bindings?: TableBinding;
}

const props = defineProps<TableProps>();

// 模拟数据
const mockData = [
  {
    orderNo: 'DD2024030100001',
    status: '执行中',
    fromArea: '华东',
    fromStore: 'DAZZLE南京新百店',
    toStore: 'DAZZLE上海港汇店'
  },
  {
    orderNo: 'DD2024030100002',
    status: '已完成',
    fromArea: '华北',
    fromStore: 'DAZZLE北京SKP店',
    toStore: 'DAZZLE天津恒隆店'
  }
];

const currentPage = ref(1);
const pageSize = computed(() => props.pagination?.pageSize || 10);
const total = ref(mockData.length);

const tableData = computed(() => {
  // 优先使用传入的数据
  const data = props.dataSource || mockData;
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return data.slice(start, end);
});

const getCellValue = (row: Record<string, any>, column: TableColumn) => {
  return row[column.dataIndex];
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
};
</script>

<style scoped>
.sd-table {
  width: 100%;
  overflow: auto;
  background: #fff;
  border-radius: 2px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 16px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

th {
  background: #fafafa;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  transition: background 0.3s ease;
  font-size: 14px;
  position: relative;
}

tbody tr:hover {
  background-color: #e6f7ff;
}

.table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-top: 1px solid #f0f0f0;
}

.pagination-info {
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
}

.pagination-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.pagination-buttons button {
  padding: 4px 12px;
  border: 1px solid #d9d9d9;
  background: #fff;
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.3s;
  color: rgba(0, 0, 0, 0.65);
  font-size: 14px;
  line-height: 1.5715;
}

.pagination-buttons button:hover:not(:disabled) {
  color: #40a9ff;
  border-color: #40a9ff;
}

.pagination-buttons button:disabled {
  cursor: not-allowed;
  color: rgba(0, 0, 0, 0.25);
  background-color: #f5f5f5;
  border-color: #d9d9d9;
}

.page-number {
  padding: 0 12px;
  color: rgba(0, 0, 0, 0.85);
}

.highlighted-column {
  color: rgb(24, 144, 255);
  font-weight: 500;
}

tbody tr td.highlighted-column {
  color: rgb(24, 144, 255);
}

tbody tr:hover td.highlighted-column {
  color: rgb(24, 144, 255);
}

.text-left {
  text-align: left;
}

.text-center {
  text-align: center;
}

.text-right {
  text-align: right;
}
</style> 