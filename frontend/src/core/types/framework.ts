// 应用配置类型定义
export interface AppConfig {
  layout: LayoutConfig;
  router: RouterConfig;
  state: StateConfig;
}

// 布局配置
export interface LayoutConfig {
  header: HeaderConfig;
  sider: SiderConfig;
  content: ContentConfig;
}

// 头部配置
export interface HeaderConfig {
  height: number;
  fixed: boolean;
  components: {
    logo: LogoConfig;
    userInfo: UserInfoConfig;
    globalSearch?: SearchConfig;
  };
}

// 侧边栏配置
export interface SiderConfig {
  width: number;
  collapsible: boolean;
  theme: 'light' | 'dark';
}

// 内容区配置
export interface ContentConfig {
  padding: number;
  tabMode: 'multi' | 'single';
}

// 路由配置
export interface RouterConfig {
  mode: 'hash' | 'history';
  routes: RouteConfig[];
}

// 路由项配置
export interface RouteConfig {
  id: string;
  path: string;
  pageKey: string;
  title: string;
  icon?: string;
  children?: RouteConfig[];
}

// 状态配置
export interface StateConfig {
  persist: boolean;
  defaultState: Record<string, any>;
}

// Logo配置
export interface LogoConfig {
  src: string;
  alt?: string;
  width?: number;
  height?: number;
}

// 用户信息配置
export interface UserInfoConfig {
  avatar?: string;
  name: string;
  role?: string;
}

// 搜索配置
export interface SearchConfig {
  placeholder?: string;
  width?: number;
} 