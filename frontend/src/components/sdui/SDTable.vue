<template>
  <div class="sd-table" :style="style">
    <!-- 表格标题 -->
    <div v-if="properties.title" class="sd-table-title">
      {{ properties.title }}
    </div>

    <!-- 表格工具栏 -->
    <div v-if="properties.showToolbar" class="sd-table-toolbar">
      <div class="sd-table-toolbar-left">
        <slot name="toolbar-left"></slot>
      </div>
      <div class="sd-table-toolbar-right">
        <slot name="toolbar-right"></slot>
      </div>
    </div>

    <!-- 表格主体 -->
    <div class="sd-table-container" :class="{ 'sd-table-loading': loading }">
      <table>
        <thead>
          <tr>
            <!-- 选择列 -->
            <th v-if="properties.selectable" class="sd-table-checkbox-col">
              <input type="checkbox" :checked="isAllSelected" @change="handleSelectAll" />
            </th>

            <!-- 数据列 -->
            <th v-for="column in columns" :key="column.key" :style="{ width: column.width }" :class="{
              'sortable': column.sortable,
              'sorted-asc': sortField === column.key && sortOrder === 'asc',
              'sorted-desc': sortField === column.key && sortOrder === 'desc'
            }" @click="handleHeaderClick(column)">
              {{ column.title }}
              <span v-if="column.sortable" class="sort-icon"></span>
            </th>

            <!-- 操作列 -->
            <th v-if="hasActions" class="sd-table-action-col">
              操作
            </th>
          </tr>
        </thead>

        <tbody>
          <tr v-if="loading && tableData.length === 0">
            <td :colspan="totalColumns" class="sd-table-loading-cell">
              <div class="sd-table-loading-spinner"></div>
            </td>
          </tr>

          <tr v-else-if="tableData.length === 0">
            <td :colspan="totalColumns" class="sd-table-empty-cell">
              {{ properties.emptyText || '暂无数据' }}
            </td>
          </tr>

          <tr v-for="(row, rowIndex) in tableData" :key="row.id || rowIndex" :class="{ 'selected': isRowSelected(row) }"
            @click="handleRowClick(row, rowIndex)">
            <!-- 选择框 -->
            <td v-if="properties.selectable" class="sd-table-checkbox-col">
              <input type="checkbox" :checked="isRowSelected(row)" @change="handleSelectRow(row, $event)" @click.stop />
            </td>

            <!-- 数据单元格 -->
            <td v-for="column in columns" :key="column.key">
              <!-- 使用渲染器配置 -->
              <template v-if="column.render">
                <!-- 标签渲染 -->
                <template v-if="column.render.type === 'tag'">
                  <span class="sd-tag" :class="`sd-tag-${getTagColor(row, column)}`">
                    {{ getTagText(row, column) }}
                  </span>
                </template>
                <!-- 其他渲染类型可在此添加 -->
                <template v-else>
                  {{ getCellValue(row, column) }}
                </template>
              </template>

              <!-- 使用自定义插槽 -->
              <slot v-else-if="column.customRender" :name="`column-${column.key}`" :row="row" :index="rowIndex"
                :column="column">
                {{ getCellValue(row, column) }}
              </slot>

              <!-- 默认渲染 -->
              <template v-else>
                {{ getCellValue(row, column) }}
              </template>
            </td>

            <!-- 操作按钮 -->
            <td v-if="hasActions" class="sd-table-action-col">
              <div class="sd-table-actions">
                <template v-for="(column, colIndex) in columns" :key="`col-${colIndex}`">
                  <template v-if="column.actions && column.actions.length > 0">
                    <button v-for="(action, actionIndex) in column.actions" :key="`action-${actionIndex}`"
                      class="sd-table-action-btn" :class="{
                        'danger': action.props?.type === 'danger',
                        'primary': action.props?.type === 'primary',
                        'warning': action.props?.type === 'warning',
                        'success': action.props?.type === 'success',
                        'disabled': isActionDisabled(action, row)
                      }" @click.stop="handleTableAction(action, row, rowIndex)"
                      :disabled="isActionDisabled(action, row)">
                      {{ action.text }}
                    </button>
                  </template>
                </template>

                <button v-for="(action, actionIndex) in properties.actions" :key="actionIndex"
                  class="sd-table-action-btn" :class="{
                    'danger': action.type === 'danger',
                    'primary': action.type === 'primary',
                    'disabled': isActionDisabled(action, row)
                  }" @click.stop="handleAction(action, row, rowIndex)" :disabled="isActionDisabled(action, row)">
                  {{ action.text }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 加载遮罩 -->
      <div v-if="loading && tableData.length > 0" class="sd-table-loading-mask">
        <div class="sd-table-loading-spinner"></div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="properties.pagination" class="sd-table-pagination">
      <div class="sd-table-pagination-total" v-if="properties.showTotal">
        共 {{ totalItems }} 条
      </div>

      <div class="sd-table-pagination-controls">
        <button class="sd-table-pagination-btn" :disabled="currentPage <= 1" @click="handlePageChange(currentPage - 1)">
          上一页
        </button>

        <div class="sd-table-pagination-info">
          {{ currentPage }} / {{ totalPages }}
        </div>

        <button class="sd-table-pagination-btn" :disabled="currentPage >= totalPages"
          @click="handlePageChange(currentPage + 1)">
          下一页
        </button>
      </div>

      <div class="sd-table-pagination-size">
        <select v-if="properties.showSizeChanger" v-model="internalPageSize">
          <option v-for="size in pageSizeOptions" :key="size" :value="size">
            {{ size }} 条/页
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';

// 定义组件属性
const props = defineProps({
  id: {
    type: String,
    required: true
  },
  properties: {
    type: Object,
    default: () => ({})
  },
  style: {
    type: Object,
    default: () => ({})
  },
  events: {
    type: Object,
    default: () => ({})
  }
});

// 定义事件
const emit = defineEmits(['action']);

// 内部状态
const loading = ref(false);
const tableData = ref<any[]>([]);
const selectedRows = ref<any[]>([]);
const sortField = ref('');
const sortOrder = ref('');
const currentPage = ref(1);
const internalPageSize = ref(props.properties.pageSize || 10);
const totalItems = ref(0);

// 计算属性
const columns = computed(() => props.properties.columns || []);
const hasActions = computed(() => props.properties.actions && props.properties.actions.length > 0);
const totalColumns = computed(() => {
  let count = columns.value.length;
  if (props.properties.selectable) count++;
  if (hasActions.value) count++;
  return count;
});
const isAllSelected = computed(() => {
  return tableData.value.length > 0 && selectedRows.value.length === tableData.value.length;
});
const pageSizeOptions = computed(() => props.properties.pageSizeOptions || [10, 20, 50, 100]);
const totalPages = computed(() => {
  if (totalItems.value === 0) return 1;
  return Math.ceil(totalItems.value / internalPageSize.value);
});

// 初始化
onMounted(async () => {
  // 设置排序初始值
  if (props.properties.defaultSort) {
    sortField.value = props.properties.defaultSort.field;
    sortOrder.value = props.properties.defaultSort.order || 'asc';
  }

  // 设置分页初始值
  if (props.properties.pagination) {
    currentPage.value = props.properties.defaultPage || 1;
    totalItems.value = props.properties.totalItems || 0;
  }

  // 加载数据
  if (props.properties.data) {
    // 如果已传入静态数据
    tableData.value = props.properties.data;
    totalItems.value = props.properties.data.length;
  } else {
    // 如果需要从API加载数据
    await loadData();
  }
});

// 加载数据
const loadData = async () => {
  // 如果没有定义加载方法，则不执行
  if (!props.events?.onLoadData && !props.properties.onLoadData) {
    console.warn('Table component: No load data method provided');
    return;
  }

  try {
    loading.value = true;

    // 触发加载数据事件
    emit('action', {
      type: 'loadData',
      componentId: props.id,
      params: {
        page: currentPage.value,
        pageSize: internalPageSize.value,
        sortField: sortField.value,
        sortOrder: sortOrder.value
      },
      event: props.events?.onLoadData || props.properties.onLoadData
    });

    // 注意：实际数据应该通过事件回调获取
    // 这里模拟一个延迟来演示加载效果
    await new Promise(resolve => setTimeout(resolve, 500));

    // 模拟数据获取
    if (props.properties.mockData) {
      // 模拟排序
      let sortedData = [...props.properties.mockData];
      if (sortField.value) {
        sortedData.sort((a, b) => {
          const aValue = a[sortField.value];
          const bValue = b[sortField.value];

          if (aValue === bValue) return 0;
          const compareResult = aValue < bValue ? -1 : 1;
          return sortOrder.value === 'asc' ? compareResult : -compareResult;
        });
      }

      // 模拟分页
      const startIndex = (currentPage.value - 1) * internalPageSize.value;
      const endIndex = startIndex + internalPageSize.value;
      tableData.value = sortedData.slice(startIndex, endIndex);
      totalItems.value = props.properties.mockData.length;
    }

  } catch (error) {
    console.error('Failed to load table data:', error);
    emit('action', {
      type: 'error',
      componentId: props.id,
      error
    });
  } finally {
    loading.value = false;
  }
};

// 获取单元格值
const getCellValue = (row, column) => {
  if (!row || !column || !column.dataIndex) return '';

  // 处理嵌套字段，如 'user.name'
  if (column.dataIndex.includes('.')) {
    const keys = column.dataIndex.split('.');
    let value = row;
    for (const key of keys) {
      value = value?.[key];
      if (value === undefined || value === null) return '';
    }
    return value;
  }

  // 处理数组字段
  if (Array.isArray(row[column.dataIndex])) {
    // 如果有render配置且fieldName指定了要显示的字段
    if (column.render && column.render.fieldName) {
      return row[column.dataIndex].map(item => item[column.render.fieldName]).join(', ');
    }
    return row[column.dataIndex].join(', ');
  }

  return row[column.dataIndex] !== undefined ? row[column.dataIndex] : '';
};

// 获取标签颜色
const getTagColor = (row, column) => {
  if (!column.render) return 'default';

  const value = getCellValue(row, column);

  // 处理options配置的情况
  if (column.render.options && Array.isArray(column.render.options)) {
    const option = column.render.options.find(opt => opt.value === value);
    return option ? option.color || 'default' : 'default';
  }

  return 'default';
};

// 获取标签文本
const getTagText = (row, column) => {
  if (!column.render) return getCellValue(row, column);

  const value = getCellValue(row, column);

  // 处理options配置的情况
  if (column.render.options && Array.isArray(column.render.options)) {
    const option = column.render.options.find(opt => opt.value === value);
    return option ? option.label : value;
  }

  // 处理fieldName指定的情况（适用于数组类型）
  if (column.render.fieldName && Array.isArray(row[column.dataIndex])) {
    return row[column.dataIndex].map(item => item[column.render.fieldName]).join(', ');
  }

  return value;
};

// 处理表格操作动作
const handleTableAction = (action, row, rowIndex) => {
  if (action.events && action.events.click) {
    emit('action', {
      type: 'tableAction',
      action: action.events.click,
      data: { row, rowIndex }
    });
  }
};

// 处理表头点击 (排序)
const handleHeaderClick = (column: any) => {
  if (!column.sortable) return;

  if (sortField.value === column.key) {
    // 切换排序顺序
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    // 设置新的排序字段
    sortField.value = column.key;
    sortOrder.value = 'asc';
  }

  // 重新加载数据
  if (props.properties.remoteSort !== false) {
    currentPage.value = 1;
    loadData();
  } else {
    // 客户端排序
    // TODO: 实现客户端排序
  }
};

// 处理行点击
const handleRowClick = (row: any, index: number) => {
  if (props.events?.onRowClick || props.properties.onRowClick) {
    emit('action', {
      type: 'rowClick',
      componentId: props.id,
      row,
      index,
      event: props.events?.onRowClick || props.properties.onRowClick
    });
  }

  // 如果启用了单击选择
  if (props.properties.selectable && props.properties.clickToSelect) {
    handleSelectRow(row);
  }
};

// 检查行是否被选中
const isRowSelected = (row: any) => {
  if (!props.properties.rowKey) {
    return selectedRows.value.includes(row);
  }

  const rowKey = props.properties.rowKey;
  return selectedRows.value.some(item => item[rowKey] === row[rowKey]);
};

// 处理选择行
const handleSelectRow = (row: any, event?: Event) => {
  const checked = event ? (event.target as HTMLInputElement).checked : !isRowSelected(row);

  if (checked && !isRowSelected(row)) {
    // 单选模式
    if (props.properties.selectMode === 'single') {
      selectedRows.value = [row];
    } else {
      // 多选模式
      selectedRows.value = [...selectedRows.value, row];
    }
  } else if (!checked && isRowSelected(row)) {
    // 取消选择
    if (props.properties.rowKey) {
      const rowKey = props.properties.rowKey;
      selectedRows.value = selectedRows.value.filter(item => item[rowKey] !== row[rowKey]);
    } else {
      selectedRows.value = selectedRows.value.filter(item => item !== row);
    }
  }

  // 触发选择变化事件
  if (props.events?.onSelectionChange || props.properties.onSelectionChange) {
    emit('action', {
      type: 'selectionChange',
      componentId: props.id,
      selection: selectedRows.value,
      event: props.events?.onSelectionChange || props.properties.onSelectionChange
    });
  }
};

// 处理全选
const handleSelectAll = (event: Event) => {
  const checked = (event.target as HTMLInputElement).checked;

  if (checked) {
    selectedRows.value = [...tableData.value];
  } else {
    selectedRows.value = [];
  }

  // 触发选择变化事件
  if (props.events?.onSelectionChange || props.properties.onSelectionChange) {
    emit('action', {
      type: 'selectionChange',
      componentId: props.id,
      selection: selectedRows.value,
      event: props.events?.onSelectionChange || props.properties.onSelectionChange
    });
  }
};

// 处理分页变化
const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value) return;

  currentPage.value = page;
  loadData();

  // 触发分页变化事件
  if (props.events?.onPageChange || props.properties.onPageChange) {
    emit('action', {
      type: 'pageChange',
      componentId: props.id,
      page,
      pageSize: internalPageSize.value,
      event: props.events?.onPageChange || props.properties.onPageChange
    });
  }
};

// 检查操作按钮是否禁用
const isActionDisabled = (action: any, row: any) => {
  if (typeof action.disabled === 'function') {
    return action.disabled(row);
  }
  return !!action.disabled;
};

// 处理表格操作
const handleAction = (action: any, row: any, rowIndex: number) => {
  if (isActionDisabled(action, row)) return;

  emit('action', {
    type: 'tableAction',
    componentId: props.id,
    action: action.key || action.text,
    row,
    rowIndex,
    event: action.onClick || props.events?.onAction || props.properties.onAction
  });
};

// 重新加载数据
const refresh = () => {
  loadData();
};

// 清除选择
const clearSelection = () => {
  selectedRows.value = [];
};

// 监听页大小变化
watch(internalPageSize, (newSize) => {
  // 重置到第一页
  currentPage.value = 1;
  loadData();

  // 触发页大小变化事件
  if (props.events?.onPageSizeChange || props.properties.onPageSizeChange) {
    emit('action', {
      type: 'pageSizeChange',
      componentId: props.id,
      pageSize: newSize,
      event: props.events?.onPageSizeChange || props.properties.onPageSizeChange
    });
  }
});

// 监听数据变化
watch(() => props.properties.data, (newData) => {
  if (newData) {
    tableData.value = newData;
    totalItems.value = newData.length;
  }
});

// 向父组件暴露方法
defineExpose({
  refresh,
  clearSelection,
  getSelectedRows: () => selectedRows.value
});
</script>

<style scoped>
.sd-table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--table-bg, #fff);
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* 添加标签样式 */
.sd-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  line-height: 20px;
  white-space: nowrap;
  margin-right: 4px;
  margin-bottom: 4px;
}

.sd-tag-default {
  background-color: #f5f5f5;
  color: #666;
}

.sd-tag-primary {
  background-color: #e6f7ff;
  color: #1890ff;
}

.sd-tag-success {
  background-color: #f6ffed;
  color: #52c41a;
}

.sd-tag-warning {
  background-color: #fffbe6;
  color: #faad14;
}

.sd-tag-danger {
  background-color: #fff1f0;
  color: #f5222d;
}

/* 其他现有样式 */
.sd-table-title {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 16px;
}

.sd-table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #fff;
  border-bottom: 1px solid #ebeef5;
}

.sd-table-container {
  position: relative;
  overflow: auto;
}

.sd-table table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 14px;
}

.sd-table th,
.sd-table td {
  padding: 12px 8px;
  border-bottom: 1px solid #ebeef5;
  transition: background-color 0.2s;
}

.sd-table th {
  background-color: #f5f7fa;
  font-weight: 500;
  color: #606266;
  white-space: nowrap;
  user-select: none;
  position: relative;
}

.sd-table th.sortable {
  cursor: pointer;
}

.sd-table th.sortable:hover {
  background-color: #e9ecf2;
}

.sd-table th.sortable .sort-icon {
  display: inline-block;
  width: 0;
  height: 0;
  border: 5px solid transparent;
  border-bottom-color: #c0c4cc;
  position: absolute;
  top: 50%;
  right: 8px;
  margin-top: -10px;
}

.sd-table th.sortable .sort-icon::after {
  content: '';
  display: inline-block;
  width: 0;
  height: 0;
  border: 5px solid transparent;
  border-top-color: #c0c4cc;
  position: absolute;
  right: -5px;
  top: 7px;
}

.sd-table th.sorted-asc .sort-icon {
  border-bottom-color: #409eff;
}

.sd-table th.sorted-desc .sort-icon::after {
  border-top-color: #409eff;
}

.sd-table tr:hover td {
  background-color: #f5f7fa;
}

.sd-table tr.selected td {
  background-color: #ecf5ff;
}

.sd-table-checkbox-col {
  width: 40px;
  text-align: center;
}

.sd-table-action-col {
  width: 1px;
  white-space: nowrap;
}

.sd-table-actions {
  display: flex;
  gap: 8px;
}

.sd-table-action-btn {
  padding: 4px 8px;
  background: transparent;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
}

.sd-table-action-btn:hover {
  color: #409eff;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.sd-table-action-btn.primary {
  color: #409eff;
  border-color: #409eff;
}

.sd-table-action-btn.primary:hover {
  color: #fff;
  background-color: #409eff;
}

.sd-table-action-btn.danger {
  color: #f56c6c;
  border-color: #f56c6c;
}

.sd-table-action-btn.danger:hover {
  color: #fff;
  background-color: #f56c6c;
}

.sd-table-action-btn.disabled {
  color: #c0c4cc;
  border-color: #e4e7ed;
  cursor: not-allowed;
  background-color: #f5f7fa;
}

.sd-table-loading-cell,
.sd-table-empty-cell {
  text-align: center;
  padding: 40px 0;
  color: #909399;
}

.sd-table-loading-spinner {
  display: inline-block;
  width: 24px;
  height: 24px;
  border: 2px solid #409eff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: table-spinner 0.8s linear infinite;
}

.sd-table-loading-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.sd-table-pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  border-top: 1px solid #ebeef5;
  background-color: #fff;
}

.sd-table-pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sd-table-pagination-btn {
  padding: 6px 12px;
  background-color: #fff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.sd-table-pagination-btn:hover:not(:disabled) {
  color: #409eff;
  border-color: #c6e2ff;
}

.sd-table-pagination-btn:disabled {
  color: #c0c4cc;
  cursor: not-allowed;
}

.sd-table-pagination-info {
  font-size: 14px;
  color: #606266;
}

.sd-table-pagination-size select {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
}

@keyframes table-spinner {
  to {
    transform: rotate(360deg);
  }
}
</style>