<template>
  <div class="sd-card" :style="style">
    <div class="card-header">
      <div class="card-title">{{ title }}</div>
      <div class="card-extra" v-if="$slots.extra">
        <slot name="extra"></slot>
      </div>
    </div>
    <div class="card-content">
      <div v-if="value" class="card-value" :class="{ 'trend-up': trend === 'up', 'trend-down': trend === 'down' }">
        {{ value }}
      </div>
      <slot></slot>
      
      <div v-if="chart && chartData" class="card-chart">
        <SDBarChart v-if="chart === 'barChart'" :data="chartData" />
      </div>
    </div>
    <div v-if="footer" class="card-footer">
      <span>{{ footer }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import SDBarChart from './SDBarChart.vue';

interface Props {
  title?: string;
  value?: string;
  footer?: string;
  style?: Record<string, string>;
  trend?: 'up' | 'down' | null;
  chart?: string;
  chartData?: any[];
}

const props = defineProps<Props>();
</script>

<style scoped>
.sd-card {
  width: 100%;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
}

.card-content {
  flex: 1;
}

.card-value {
  font-size: 24px;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.85);
  margin-bottom: 8px;
}

.card-value.trend-up {
  color: #52c41a;
}

.card-value.trend-down {
  color: #f5222d;
}

.card-chart {
  height: 100%;
  min-height: 120px;
}

.card-footer {
  margin-top: 16px;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
}
</style> 