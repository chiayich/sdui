<template>
  <div class="sd-toolbar" :style="props.style">
    <div class="toolbar-left">
      <template v-if="props.items && props.items.length > 0">
        <div v-for="item in props.items" :key="item.id" class="toolbar-item">
          <template v-if="item.type === 'selection'">
            <div class="selection-wrapper">
              <span class="selection-label">{{ item.text }}:</span>
              <label v-for="option in item.props?.options" :key="option" class="selection-option">
                <input type="checkbox" /> {{ option }}
              </label>
            </div>
          </template>
        </div>
      </template>
    </div>
    <div class="toolbar-right">
      <template v-if="props.actions && props.actions.length > 0">
        <div v-for="action in props.actions" :key="action.id" class="toolbar-action">
          <button 
            class="toolbar-button" 
            :class="{ 'primary': action.props?.type === 'primary' }"
          >
            {{ action.text }}
          </button>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
interface ToolbarItem {
  id: string;
  type: string;
  text?: string;
  props?: Record<string, any>;
}

interface ToolbarAction {
  id: string;
  text: string;
  props?: {
    type?: string;
    [key: string]: any;
  };
}

interface Props {
  items?: ToolbarItem[];
  actions?: ToolbarAction[];
  style?: Record<string, string>;
}

const props = defineProps<Props>();
</script>

<style scoped>
.sd-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  background: #fff;
  margin-bottom: 8px;
  border-radius: 0;
  border: 1px solid #f0f0f0;
}

.toolbar-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toolbar-item {
  display: flex;
  align-items: center;
}

.selection-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selection-label {
  font-weight: 400;
  margin-right: 8px;
  color: rgba(0, 0, 0, 0.85);
}

.selection-option {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  user-select: none;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.toolbar-button {
  padding: 0 15px;
  border-radius: 2px;
  border: 1px solid #d9d9d9;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  height: 32px;
  transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
  color: rgba(0, 0, 0, 0.65);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1.5715;
}

.toolbar-button.primary {
  background: rgb(24, 144, 255);
  border-color: rgb(24, 144, 255);
  color: #fff;
}

.toolbar-button:hover {
  color: #40a9ff;
  border-color: #40a9ff;
}

.toolbar-button.primary:hover {
  background: #40a9ff;
  border-color: #40a9ff;
}
</style> 