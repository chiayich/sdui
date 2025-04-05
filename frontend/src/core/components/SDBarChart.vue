<template>
  <div class="sd-bar-chart" :style="style">
    <div v-if="title" class="chart-title">{{ title }}</div>
    <div class="chart-container">
      <div class="chart-y-axis">
        <div class="axis-label" v-for="(label, index) in yAxisLabels" :key="index">
          {{ label }}
        </div>
      </div>
      <div class="chart-content">
        <div class="chart-bars">
          <div
            v-for="(item, index) in data"
            :key="index"
            class="bar-item"
          >
            <div 
              class="bar" 
              :style="{ 
                height: `${calculateHeight(item.value)}%`,
                backgroundColor: index === activeBarIndex ? '#1890ff' : '#d9d9d9'
              }"
            >
              <div class="bar-value">{{ item.value }}</div>
            </div>
            <div class="bar-label">{{ item.category }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface ChartDataItem {
  category: string;
  value: number;
}

interface Props {
  title?: string;
  data?: ChartDataItem[];
  style?: Record<string, string>;
  activeIndex?: number;
}

const props = defineProps<Props>();

// 固定高亮第一个柱状图
const activeBarIndex = ref(0);

// 计算Y轴标签
const yAxisLabels = computed(() => {
  if (!props.data || props.data.length === 0) return [0];
  
  const maxValue = Math.max(...props.data.map(item => item.value));
  const step = Math.ceil(maxValue / 4);
  const labels = [];
  
  for (let i = 0; i <= 4; i++) {
    labels.unshift(i * step);
  }
  
  return labels;
});

// 计算柱状图高度百分比
const calculateHeight = (value: number) => {
  if (!props.data || props.data.length === 0) return 0;
  
  const maxValue = Math.max(...props.data.map(item => item.value));
  if (maxValue === 0) return 0;
  
  return (value / maxValue) * 100;
};
</script>

<style scoped>
.sd-bar-chart {
  width: 100%;
  height: 100%;
  background-color: #fff;
  border-radius: 2px;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.chart-title {
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  margin-bottom: 16px;
}

.chart-container {
  flex: 1;
  display: flex;
  align-items: stretch;
}

.chart-y-axis {
  width: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding-bottom: 20px;
}

.axis-label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  text-align: right;
  padding-right: 4px;
}

.chart-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chart-bars {
  flex: 1;
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  padding-bottom: 20px;
}

.bar-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 8%;
  min-width: 16px;
}

.bar {
  width: 100%;
  background-color: #d9d9d9;
  border-radius: 2px 2px 0 0;
  position: relative;
  transition: all 0.3s;
}

.bar-value {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: -20px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
}

.bar-label {
  margin-top: 4px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
  text-align: center;
  white-space: nowrap;
}
</style> 