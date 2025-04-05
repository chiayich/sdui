// 页面配置
export interface PageConfig {
  pageKey: string;
  version: string;
  title: string;
  layout?: {
    type: string;
    header?: HeaderConfig;
    sider?: SiderConfig;
  };
  components: ComponentConfig[];
  dataSources?: Record<string, DataSourceConfig>;
  state?: Record<string, StateConfig>;
}

// 页面头部配置
export interface HeaderConfig {
  title?: string;
  subtitle?: string;
  logo?: string;
  userInfo?: {
    name: string;
    role: string;
  };
  breadcrumb?: boolean;
  actions?: ActionConfig[];
  style?: Record<string, string>;
}

// 侧边栏配置
export interface SiderConfig {
  width: number;
  theme: 'light' | 'dark';
  menu: MenuItem[];
}

// 菜单项配置
export interface MenuItem {
  key: string;
  title: string;
  icon?: string;
  active?: boolean;
  expanded?: boolean;
  children?: MenuItem[];
}

// 页面布局配置
export interface PageLayoutConfig {
  type: 'standard' | 'custom' | 'blank';
  header?: {
    title?: string;
    breadcrumb?: boolean;
    actions?: ActionConfig[];
  };
}

// 页面状态配置
export interface PageStateConfig {
  [key: string]: {
    type: 'string' | 'number' | 'boolean' | 'object' | 'array';
    default?: any;
    persist?: boolean;
  };
}

// 数据源配置
export interface DataSourceConfig {
  type: string;
  api?: string;
  method?: string;
  params?: Record<string, any>;
  cache?: {
    enabled: boolean;
    duration: number;
  };
}

// 组件配置
export interface ComponentConfig {
  type: string;
  id: string;
  props?: Record<string, any>;
  children?: ComponentConfig[];
  bindings?: Record<string, BindingConfig>;
  events?: Record<string, ActionConfig[]>;
}

// 动作配置
export interface ActionConfig {
  type: string;
  action?: string;
  target?: string;
  value?: any;
}

export interface BindingConfig {
  type: 'state' | 'dataSource' | 'compute';
  source: string;
}

export interface StateConfig {
  type: string;
  default: any;
} 