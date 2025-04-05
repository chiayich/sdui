<template>
    <div class="table-page">
        <!-- 筛选器区域 -->
        <div class="filter-section">
            <div class="filter-container">
                <div class="filter-fields">
                    <div class="filter-field" v-for="field in filterFields" :key="field.key">
                        <label>{{ field.label }}</label>
                        <input v-if="field.type === 'text'" v-model="filterForm[field.key]"
                            :placeholder="field.placeholder" class="filter-input" />
                        <select v-else-if="field.type === 'select'" v-model="filterForm[field.key]"
                            class="filter-select">
                            <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
                                {{ opt.label }}
                            </option>
                        </select>
                        <input v-else-if="field.type === 'date'" type="date" v-model="filterForm[field.key]"
                            class="filter-input" />
                    </div>
                </div>
                <div class="filter-buttons">
                    <SDButton type="primary" @click="handleSearch">搜索</SDButton>
                    <SDButton @click="resetFilters">重置</SDButton>
                </div>
            </div>
        </div>

        <!-- 表格区域 -->
        <div class="table-section">
            <div class="table-header">
                <SDButton type="primary" @click="handleAdd">新增</SDButton>
            </div>
            <table class="sd-table">
                <thead>
                    <tr>
                        <th v-for="col in columns" :key="col.prop" :style="{ width: col.width }">
                            {{ col.label }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="loading">
                        <td :colspan="columns.length" class="loading-cell">加载中...</td>
                    </tr>
                    <tr v-else-if="tableData.length === 0">
                        <td :colspan="columns.length" class="empty-cell">暂无数据</td>
                    </tr>
                    <tr v-else v-for="row in tableData" :key="row.id">
                        <td v-for="col in columns" :key="col.prop">
                            <template v-if="col.prop === 'actions'">
                                <div class="action-buttons">
                                    <SDButton type="primary" size="small" @click="handleEdit(row)">编辑</SDButton>
                                    <SDButton type="danger" size="small" @click="handleDelete(row)">删除</SDButton>
                                </div>
                            </template>
                            <template v-else>
                                {{ typeof col.prop === 'string' ? row[col.prop as keyof TableData] : '' }}
                            </template>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- 新增/编辑对话框 -->
        <SDDialog v-model="dialogVisible" :title="dialogTitle" width="500px" @confirm="handleDialogConfirm"
            @cancel="handleDialogCancel">
            <SDForm ref="formRef" :fields="formFields" v-model="formData" />
        </SDDialog>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { TableColumn, TableData } from '@/types/sdui'

const baseURL = 'http://localhost:8000';

// 筛选表单配置
const filterFields = [
    {
        key: 'name',
        label: '名称',
        type: 'text',
        placeholder: '请输入名称'
    },
    {
        key: 'status',
        label: '状态',
        type: 'select',
        placeholder: '请选择状态',
        options: [
            { label: '全部', value: '' },
            { label: '启用', value: 'active' },
            { label: '禁用', value: 'inactive' }
        ]
    },
    {
        key: 'createDate',
        label: '创建日期',
        type: 'date',
        placeholder: '请选择日期'
    }
]

// 表格列配置
const columns: TableColumn[] = [
    { prop: 'name', label: '名称', width: '150' },
    { prop: 'status', label: '状态', width: '100' },
    { prop: 'createDate', label: '创建日期', width: '180' },
    { prop: 'description', label: '描述' },
    {
        prop: 'actions',
        label: '操作',
        width: '150',
        render: (row: TableData) => ({
            type: 'button-group',
            buttons: [
                {
                    type: 'primary',
                    text: '编辑',
                    onClick: () => handleEdit(row)
                },
                {
                    type: 'danger',
                    text: '删除',
                    onClick: () => handleDelete(row)
                }
            ]
        })
    }
]

// 表单配置
const formFields = [
    {
        key: 'name',
        label: '名称',
        type: 'text',
        required: true
    },
    {
        key: 'status',
        label: '状态',
        type: 'select',
        required: true,
        options: [
            { label: '启用', value: 'active' },
            { label: '禁用', value: 'inactive' }
        ]
    },
    {
        key: 'description',
        label: '描述',
        type: 'textarea',
        rows: 4
    }
]

// 响应式数据
interface FilterForm {
    [key: string]: string;
}

const filterForm = reactive<FilterForm>({
    name: '',
    status: '',
    createDate: ''
})

const tableData = ref<TableData[]>([])
const loading = ref(false)
const pagination = reactive({
    current: 1,
    pageSize: 10,
    total: 0
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增')
const formData = reactive<TableData>({
    name: '',
    status: '',
    description: ''
})
const formRef = ref()

// 方法
const handleSearch = async () => {
    loading.value = true;
    try {
        console.log('Sending search request:', {
            page: pagination.current,
            pageSize: pagination.pageSize,
            ...filterForm
        });

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        const response = await fetch(`${baseURL}/api/table-data`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                page: pagination.current,
                page_size: pagination.pageSize,
                name: filterForm.name || undefined,
                status: filterForm.status || undefined,
                create_date: filterForm.createDate || undefined
            }),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            console.error('Search request failed:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Error details:', errorText);
            throw new Error(`Request failed: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Search response:', data);

        tableData.value = data.items || [];
        pagination.total = data.total || 0;
    } catch (error) {
        console.error('Error fetching data:', error);
        tableData.value = [];
        pagination.total = 0;
    } finally {
        loading.value = false;
    }
}

const handleAdd = () => {
    dialogTitle.value = '新增'
    // 重置表单数据
    Object.assign(formData, {
        id: undefined,
        name: '',
        status: 'active', // 设置默认值
        description: ''
    })
    // 确保在下一个事件循环中打开对话框
    setTimeout(() => {
        dialogVisible.value = true
    }, 0)
}

const handleEdit = (row: TableData) => {
    dialogTitle.value = '编辑'
    // 重置表单数据
    Object.assign(formData, {
        id: row.id,
        name: row.name || '',
        status: row.status || 'active',
        description: row.description || ''
    })
    // 确保在下一个事件循环中打开对话框
    setTimeout(() => {
        dialogVisible.value = true
    }, 0)
}

const handleDelete = async (row: TableData) => {
    if (!confirm('确定要删除这条记录吗？')) return;

    try {
        console.log('Deleting item:', row.id);

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        const response = await fetch(`${baseURL}/api/table-data/${row.id}`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json'
            },
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            console.error('Delete request failed:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Error details:', errorText);
            throw new Error(`Request failed: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Delete response:', data);

        handleSearch();
    } catch (error) {
        console.error('Error deleting item:', error);
    }
}

const handleDialogCancel = () => {
    dialogVisible.value = false;
    // 重置表单数据
    Object.assign(formData, {
        name: '',
        status: '',
        description: ''
    });
};

const handleDialogConfirm = async () => {
    if (!formRef.value) return;

    try {
        const valid = await formRef.value.validate();
        if (!valid) {
            console.log('Form validation failed');
            return;
        }

        console.log('Submitting form data:', formData);

        const url = formData.id
            ? `${baseURL}/api/table-data/${formData.id}`
            : `${baseURL}/api/table-data/create`;

        const method = formData.id ? 'PUT' : 'POST';

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 10000);

        const response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            console.error('Submit request failed:', response.status, response.statusText);
            const errorText = await response.text();
            console.error('Error details:', errorText);
            throw new Error(`Request failed: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('Submit response:', data);

        dialogVisible.value = false;
        handleSearch();
    } catch (error) {
        console.error('Error submitting form:', error);
    }
}

const resetFilters = () => {
    Object.assign(filterForm, {
        name: '',
        status: '',
        createDate: ''
    })
    handleSearch()
}

const handlePageChange = (page: number) => {
    pagination.current = page
    handleSearch()
}
</script>

<style scoped>
:root {
    --ant-primary-color: #1890ff;
    --ant-primary-hover: #40a9ff;
    --ant-border-color: #f0f0f0;
    --ant-background-color: #fafafa;
    --ant-text-color: rgba(0, 0, 0, 0.85);
    --ant-text-color-secondary: rgba(0, 0, 0, 0.45);
}

.table-page {
    padding: 24px;
    background: var(--ant-background-color);
    min-height: 100%;
}

.filter-section {
    background: #fff;
    padding: 24px;
    border-radius: 2px;
    margin-bottom: 16px;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

.filter-container {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.filter-fields {
    display: flex;
    flex: 1;
    gap: 16px;
    flex-wrap: wrap;
}

.filter-field {
    display: flex;
    align-items: center;
    gap: 8px;
}

.filter-field label {
    white-space: nowrap;
    color: var(--ant-text-color);
    font-size: 14px;
}

.filter-input,
.filter-select {
    height: 32px;
    padding: 4px 11px;
    border: 1px solid var(--ant-border-color);
    border-radius: 2px;
    width: 200px;
    outline: none;
    transition: all 0.3s;
    color: var(--ant-text-color);
    background-color: #fff;
}

.filter-input:hover,
.filter-select:hover {
    border-color: var(--ant-primary-hover);
}

.filter-input:focus,
.filter-select:focus {
    border-color: var(--ant-primary-hover);
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.filter-buttons {
    display: flex;
    gap: 8px;
    margin-left: auto;
}

.table-section {
    background: #fff;
    padding: 24px;
    border-radius: 2px;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
}

.table-header {
    margin-bottom: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sd-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 2px;
    border: 1px solid var(--ant-border-color);
}

.sd-table th,
.sd-table td {
    padding: 16px;
    border-bottom: 1px solid var(--ant-border-color);
    text-align: left;
    font-size: 14px;
    color: var(--ant-text-color);
    transition: background 0.3s;
}

.sd-table th {
    background: var(--ant-background-color);
    color: var(--ant-text-color);
    font-weight: 500;
    white-space: nowrap;
    transition: background 0.3s;
    padding: 16px;
    border-bottom: 1px solid var(--ant-border-color);
}

.sd-table tbody tr:hover {
    background-color: #fafafa;
}

.loading-cell,
.empty-cell {
    text-align: center;
    color: var(--ant-text-color-secondary);
    padding: 48px;
    font-size: 14px;
}

.action-buttons {
    display: flex;
    gap: 8px;
}

/* Ant Design 按钮样式覆盖 */
:deep(.sd-button) {
    height: 32px;
    padding: 4px 15px;
    border-radius: 2px;
    font-size: 14px;
    border: 1px solid var(--ant-border-color);
    background: #fff;
    color: var(--ant-text-color);
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

:deep(.sd-button--primary) {
    background: var(--ant-primary-color);
    border-color: var(--ant-primary-color);
    color: #fff;
}

:deep(.sd-button--primary:hover) {
    background: var(--ant-primary-hover);
    border-color: var(--ant-primary-hover);
}

:deep(.sd-button--danger) {
    color: #ff4d4f;
    border-color: #ff4d4f;
}

:deep(.sd-button--danger:hover) {
    background: #fff1f0;
    border-color: #ff7875;
    color: #ff7875;
}

:deep(.sd-button--small) {
    height: 24px;
    padding: 0 7px;
    font-size: 14px;
}

/* 对话框样式 */
:deep(.sd-dialog) {
    border-radius: 2px;
    box-shadow: 0 3px 6px -4px rgba(0, 0, 0, 0.12),
        0 6px 16px 0 rgba(0, 0, 0, 0.08),
        0 9px 28px 8px rgba(0, 0, 0, 0.05);
}

:deep(.sd-dialog__header) {
    padding: 16px 24px;
    border-bottom: 1px solid var(--ant-border-color);
}

:deep(.sd-dialog__body) {
    padding: 24px;
}

:deep(.sd-dialog__footer) {
    padding: 10px 16px;
    border-top: 1px solid var(--ant-border-color);
    background: #fff;
}

/* 表单样式 */
:deep(.sd-form) {
    font-size: 14px;
}

:deep(.sd-form__label) {
    color: var(--ant-text-color);
    font-size: 14px;
}

:deep(.sd-form__input),
:deep(.sd-form__select),
:deep(.sd-form__textarea) {
    padding: 4px 11px;
    border: 1px solid var(--ant-border-color);
    border-radius: 2px;
    transition: all 0.3s;
}

:deep(.sd-form__input:hover),
:deep(.sd-form__select:hover),
:deep(.sd-form__textarea:hover) {
    border-color: var(--ant-primary-hover);
}

:deep(.sd-form__input:focus),
:deep(.sd-form__select:focus),
:deep(.sd-form__textarea:focus) {
    border-color: var(--ant-primary-hover);
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

:deep(.sd-form__error) {
    color: #ff4d4f;
    font-size: 14px;
    line-height: 1.5715;
    margin-top: 4px;
}
</style>