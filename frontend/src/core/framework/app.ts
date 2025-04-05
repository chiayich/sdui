import { App, Component, createApp, h } from 'vue';
import { AppConfig } from '../types/framework';
import { SDUIRenderer } from '../renderer';
import { createRouter, createWebHashHistory, createWebHistory, Router } from 'vue-router';
import { createPinia, Pinia } from 'pinia';

export class SDUIApp {
  private config: AppConfig;
  private renderer: SDUIRenderer;
  private app: App | null = null;
  private router: Router | null = null;
  private pinia: Pinia | null = null;

  constructor(config: AppConfig) {
    this.config = config;
    this.renderer = new SDUIRenderer();
  }

  // 注册组件
  registerComponent(type: string, component: Component): void {
    this.renderer.registerComponent(type, component);
  }

  // 初始化路由
  private initRouter(): void {
    const { mode, routes } = this.config.router;
    
    this.router = createRouter({
      history: mode === 'hash' ? createWebHashHistory() : createWebHistory(),
      routes: routes.map(route => ({
        path: route.path,
        component: () => import(`@/pages/${route.pageKey}.vue`),
        meta: {
          title: route.title,
          pageKey: route.pageKey
        }
      }))
    });
  }

  // 初始化状态管理
  private initStore(): void {
    this.pinia = createPinia();
  }

  // 初始化布局
  private async initLayout(): Promise<void> {
    // TODO: 实现布局初始化
  }

  // 启动应用
  async bootstrap(rootContainer: string | Element): Promise<void> {
    try {
      // 1. 初始化路由
      this.initRouter();

      // 2. 初始化状态管理
      this.initStore();

      // 3. 初始化布局
      await this.initLayout();

      // 4. 创建应用实例
      const AppComponent = {
        name: 'SDUIApp',
        setup() {
          return () => h('div', { class: 'sdui-app' }, [
            // TODO: 渲染应用布局
          ]);
        }
      };

      this.app = createApp(AppComponent);

      // 5. 安装插件
      if (this.router) {
        this.app.use(this.router);
      }
      if (this.pinia) {
        this.app.use(this.pinia);
      }

      // 6. 挂载应用
      this.app.mount(rootContainer);

    } catch (error) {
      console.error('Failed to bootstrap SDUI application:', error);
      throw error;
    }
  }

  // 销毁应用
  destroy(): void {
    if (this.app) {
      this.app.unmount();
      this.app = null;
    }
    this.router = null;
    this.pinia = null;
  }
} 