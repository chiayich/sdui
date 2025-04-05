<template>
  <div class="sd-date-picker" :style="style">
    <input 
      type="text" 
      class="date-input" 
      readonly
      :placeholder="placeholder || '选择日期'"
      :value="formattedValue"
      @click="togglePicker"
    />
    <div class="date-icon">📅</div>
    
    <!-- 简易日期选择面板 -->
    <div v-if="isOpen" class="date-picker-panel" @click.stop>
      <div class="date-picker-header">
        <button class="date-nav-btn" @click.stop="changeMonth(-1)">◀</button>
        <span>{{ currentYear }}年{{ currentMonth + 1 }}月</span>
        <button class="date-nav-btn" @click.stop="changeMonth(1)">▶</button>
      </div>
      <div class="date-picker-body">
        <div class="date-picker-weekdays">
          <span v-for="day in ['日', '一', '二', '三', '四', '五', '六']" :key="day">{{ day }}</span>
        </div>
        <div class="date-picker-days">
          <div 
            v-for="(day, index) in daysInMonth" 
            :key="index" 
            class="date-day"
            :class="{ 
              'empty': !day.inMonth, 
              'selected': isSelectedDay(day.date),
              'current': isCurrentDay(day.date)
            }"
            @click="selectDate(day.date)"
          >
            {{ day.day }}
          </div>
        </div>
      </div>
      <div class="date-picker-footer">
        <button class="date-today-btn" @click.stop="selectToday">今天</button>
        <button class="date-clear-btn" @click.stop="clearDate">清空</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

interface Props {
  placeholder?: string;
  style?: Record<string, string>;
  value?: string;
}

const props = defineProps<Props>();
const emit = defineEmits(['update:value']);

// 日期选择器状态
const isOpen = ref(false);
const selectedDate = ref(props.value ? new Date(props.value) : null);
const currentDate = ref(selectedDate.value || new Date());
const currentYear = computed(() => currentDate.value.getFullYear());
const currentMonth = computed(() => currentDate.value.getMonth());

// 格式化日期显示
const formattedValue = computed(() => {
  if (!props.value) return '';
  
  try {
    // 尝试解析日期并格式化
    const date = new Date(props.value);
    if (isNaN(date.getTime())) return props.value;
    
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    }).replace(/\//g, '-');
  } catch (e) {
    return props.value;
  }
});

// 生成当月的天数数组
const daysInMonth = computed(() => {
  const days = [];
  const firstDay = new Date(currentYear.value, currentMonth.value, 1);
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0);
  const daysCount = lastDay.getDate();
  
  // 前一个月的天数
  const firstDayWeekday = firstDay.getDay();
  for (let i = firstDayWeekday - 1; i >= 0; i--) {
    const day = new Date(currentYear.value, currentMonth.value, -i);
    days.push({
      day: day.getDate(),
      date: new Date(day),
      inMonth: false
    });
  }
  
  // 当月天数
  for (let i = 1; i <= daysCount; i++) {
    days.push({
      day: i,
      date: new Date(currentYear.value, currentMonth.value, i),
      inMonth: true
    });
  }
  
  // 下个月的天数
  const lastDayWeekday = lastDay.getDay();
  for (let i = 1; i < 7 - lastDayWeekday; i++) {
    const day = new Date(currentYear.value, currentMonth.value + 1, i);
    days.push({
      day: day.getDate(),
      date: new Date(day),
      inMonth: false
    });
  }
  
  return days;
});

// 切换月份
const changeMonth = (delta: number) => {
  currentDate.value = new Date(currentYear.value, currentMonth.value + delta, 1);
};

// 选择日期
const selectDate = (date: Date) => {
  selectedDate.value = date;
  const formattedDate = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  emit('update:value', formattedDate);
  isOpen.value = false;
};

// 监听value属性变化
watch(() => props.value, (newValue) => {
  if (newValue) {
    try {
      const date = new Date(newValue);
      if (!isNaN(date.getTime())) {
        selectedDate.value = date;
      }
    } catch (e) {
      // 忽略无效日期
    }
  } else {
    selectedDate.value = null;
  }
}, { immediate: true });

// 选择今天
const selectToday = () => {
  const today = new Date();
  selectDate(today);
};

// 清空日期
const clearDate = () => {
  selectedDate.value = null;
  emit('update:value', '');
  isOpen.value = false;
};

// 判断是否是选中的日期
const isSelectedDay = (date: Date) => {
  if (!selectedDate.value) return false;
  return date.getFullYear() === selectedDate.value.getFullYear() &&
         date.getMonth() === selectedDate.value.getMonth() &&
         date.getDate() === selectedDate.value.getDate();
};

// 判断是否是当天
const isCurrentDay = (date: Date) => {
  const today = new Date();
  return date.getFullYear() === today.getFullYear() &&
         date.getMonth() === today.getMonth() &&
         date.getDate() === today.getDate();
};

// 切换日期选择器
const togglePicker = () => {
  isOpen.value = !isOpen.value;
  
  // 如果有选择日期，设置当前视图为选择的月份
  if (selectedDate.value && isOpen.value) {
    currentDate.value = new Date(selectedDate.value);
  }
};

// 点击外部关闭日期选择器
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement;
  if (!target.closest('.sd-date-picker')) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  // 如果有初始值，设置选中日期
  if (props.value) {
    try {
      const date = new Date(props.value);
      if (!isNaN(date.getTime())) {
        selectedDate.value = date;
        currentDate.value = new Date(date);
      }
    } catch (e) {
      // 忽略无效日期
    }
  }
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.sd-date-picker {
  position: relative;
  width: 100%;
  min-width: 120px;
}

.date-input {
  width: 100%;
  padding: 4px 30px 4px 11px;
  height: 32px;
  line-height: 1.5;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  cursor: pointer;
  background-color: #fff;
}

.date-input:hover {
  border-color: #40a9ff;
}

.date-icon {
  position: absolute;
  right: 11px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  color: #666;
  pointer-events: none;
}

/* 日期选择面板 */
.date-picker-panel {
  position: absolute;
  top: 100%;
  left: 0;
  width: 280px;
  background: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1050;
  margin-top: 4px;
}

.date-picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid #f0f0f0;
}

.date-nav-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.date-nav-btn:hover {
  color: #1890ff;
}

.date-picker-body {
  padding: 8px;
}

.date-picker-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
  margin-bottom: 8px;
  font-weight: 500;
}

.date-picker-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.date-day {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 24px;
  border-radius: 2px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.date-day:hover {
  background-color: #f5f5f5;
}

.date-day.empty {
  color: #ccc;
}

.date-day.selected {
  background-color: #1890ff;
  color: #fff;
}

.date-day.current:not(.selected) {
  color: #1890ff;
  font-weight: 500;
}

.date-picker-footer {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  border-top: 1px solid #f0f0f0;
}

.date-today-btn, .date-clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #1890ff;
  padding: 0;
  font-size: 14px;
}

.date-today-btn:hover, .date-clear-btn:hover {
  color: #40a9ff;
}
</style> 