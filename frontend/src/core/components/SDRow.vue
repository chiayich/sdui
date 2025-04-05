<template>
  <div class="sd-row" :style="[style, { gap: `${gutter}px` }]">
    <template v-for="child in children" :key="child.id">
      <component
        :is="resolveComponent(child.type)"
        v-bind="child.props"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import SDCard from './SDCard.vue';
import SDBarChart from './SDBarChart.vue';

interface ChildComponent {
  id: string;
  type: string;
  props?: Record<string, any>;
}

interface Props {
  children?: ChildComponent[];
  style?: Record<string, string>;
  gutter?: number;
}

const props = defineProps<Props>();

const resolveComponent = (type: string) => {
  const componentMap = {
    card: SDCard,
    barChart: SDBarChart
  };
  return componentMap[type as keyof typeof componentMap] || 'div';
};
</script>

<style scoped>
.sd-row {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  margin-bottom: 16px;
}
</style> 