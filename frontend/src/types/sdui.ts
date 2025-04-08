// SDUI组件类型定义

// 样式对象
export interface UIStyle {
  [key: string]: string | number;
}

// 属性对象
export interface UIProperties {
  [key: string]: any;
  content?: string;
  label?: string;
}

// 事件对象
export interface UIEvents {
  [key: string]: UIAction;
}

// 动作类型
export interface UIAction {
  type: string;
  [key: string]: any;
  url?: string;
  target?: string;
  params?: Record<string, any>;
}

// 组件定义
export interface UIComponent {
  id: string;
  type: string;
  style?: UIStyle;
  properties?: UIProperties;
  events?: UIEvents;
  children?: UIComponent[];
}

// UI屏幕定义
export interface UIScreen {
  id: string;
  title: string;
  components: UIComponent[];
}

// UI配置响应
export interface UIConfig {
  type: "page" | "component" | "layout" | "structure";
  id: string;
  title?: string;
  content?: UIComponent[];
  layout?: Record<string, any>;
  styles?: Record<string, any>;
  metadata?: Record<string, any>;
  is_public?: boolean;
  version: number;
}

// 组件动作事件
export interface ComponentActionEvent {
  type: string;
  componentId: string;
  [key: string]: any;
} 