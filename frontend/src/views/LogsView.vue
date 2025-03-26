<template>
  <div class="logs-view">
    <h1>系统日志</h1>
    
    <div class="filters">
      <div class="filter-group">
        <label for="level-filter">日志级别:</label>
        <select id="level-filter" v-model="filters.level">
          <option value="">全部</option>
          <option v-for="level in levels" :key="level" :value="level">{{ level }}</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="source-filter">日志源:</label>
        <select id="source-filter" v-model="filters.source">
          <option value="">全部</option>
          <option v-for="source in sources" :key="source" :value="source">{{ source }}</option>
        </select>
      </div>
      
      <button @click="fetchLogs" class="refresh-btn">刷新</button>
    </div>
    
    <div class="logs-container">
      <table v-if="logs.length > 0" class="logs-table">
        <thead>
          <tr>
            <th>时间</th>
            <th>级别</th>
            <th>源</th>
            <th>消息</th>
            <th>详情</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(log, index) in logs" :key="index" :class="getLogClass(log.level)">
            <td>{{ formatTimestamp(log.timestamp) }}</td>
            <td>{{ log.level }}</td>
            <td>{{ log.source }}</td>
            <td>{{ log.message }}</td>
            <td>
              <button 
                v-if="log.metadata && Object.keys(log.metadata).length > 0" 
                @click="toggleDetails(index)" 
                class="details-btn"
              >
                {{ expandedRows.includes(index) ? '隐藏' : '查看' }}
              </button>
            </td>
          </tr>
          <template v-for="(log, index) in logs" :key="`details-${index}`">
            <tr v-if="expandedRows.includes(index)" class="details-row">
              <td colspan="5">
                <pre>{{ JSON.stringify(log.metadata, null, 2) }}</pre>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      
      <div v-else class="no-logs">
        <p>没有符合条件的日志记录</p>
      </div>
      
      <div class="pagination">
        <button 
          @click="prevPage" 
          :disabled="filters.offset === 0"
          class="pagination-btn"
        >
          上一页
        </button>
        <span>第 {{ currentPage }} 页</span>
        <button 
          @click="nextPage" 
          :disabled="logs.length < filters.limit"
          class="pagination-btn"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import axios from 'axios';
import logger from '../lib/logger';

// 日志数据
const logs = ref<any[]>([]);
const levels = ref<string[]>([]);
const sources = ref<string[]>([]);
const expandedRows = ref<number[]>([]);

// 筛选条件
const filters = reactive({
  level: '',
  source: '',
  limit: 20,
  offset: 0
});

// 计算当前页码
const currentPage = computed(() => Math.floor(filters.offset / filters.limit) + 1);

// 获取日志记录
const fetchLogs = async () => {
  try {
    const response = await axios.get('/api/logs', { params: filters });
    logs.value = response.data;
    logger.info('Fetched logs', { count: logs.value.length, filters });
  } catch (error) {
    logger.error('Failed to fetch logs', { error });
  }
};

// 获取日志级别
const fetchLevels = async () => {
  try {
    const response = await axios.get('/api/logs/levels');
    levels.value = response.data;
  } catch (error) {
    logger.error('Failed to fetch log levels', { error });
  }
};

// 获取日志源
const fetchSources = async () => {
  try {
    const response = await axios.get('/api/logs/sources');
    sources.value = response.data;
  } catch (error) {
    logger.error('Failed to fetch log sources', { error });
  }
};

// 格式化时间戳
const formatTimestamp = (timestamp: string) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

// 获取日志行的CSS类名
const getLogClass = (level: string) => {
  switch (level) {
    case 'ERROR':
      return 'log-error';
    case 'WARNING':
      return 'log-warning';
    case 'INFO':
      return 'log-info';
    case 'DEBUG':
      return 'log-debug';
    default:
      return '';
  }
};

// 切换详情展示
const toggleDetails = (index: number) => {
  if (expandedRows.value.includes(index)) {
    expandedRows.value = expandedRows.value.filter(i => i !== index);
  } else {
    expandedRows.value.push(index);
  }
};

// 上一页
const prevPage = () => {
  if (filters.offset >= filters.limit) {
    filters.offset -= filters.limit;
    fetchLogs();
  }
};

// 下一页
const nextPage = () => {
  filters.offset += filters.limit;
  fetchLogs();
};

// 初始化
onMounted(async () => {
  await Promise.all([
    fetchLevels(),
    fetchSources()
  ]);
  fetchLogs();
});
</script>

<style scoped>
.logs-view {
  padding: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.logs-container {
  margin-top: 1rem;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.logs-table th,
.logs-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.logs-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}

.log-error {
  background-color: #ffebee;
}

.log-warning {
  background-color: #fff8e1;
}

.log-info {
  background-color: #e8f5e9;
}

.log-debug {
  background-color: #e3f2fd;
}

.details-row {
  background-color: #f5f5f5;
}

.details-row pre {
  margin: 0;
  white-space: pre-wrap;
  font-size: 0.85rem;
}

.no-logs {
  text-align: center;
  padding: 2rem;
  color: #757575;
}

.pagination {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.refresh-btn,
.details-btn,
.pagination-btn {
  background-color: #336699;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.details-btn {
  background-color: #607d8b;
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
}

.pagination-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style> 