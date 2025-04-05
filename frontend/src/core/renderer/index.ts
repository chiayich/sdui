import { ComponentConfig, PageConfig } from '../types/page';
import { Component, defineComponent, h, VNode } from 'vue';

export class ComponentRegistry {
  private components: Map<string, Component> = new Map();

  register(type: string, component: Component): void {
    this.components.set(type, component);
  }

  get(type: string): Component | undefined {
    return this.components.get(type);
  }

  has(type: string): boolean {
    return this.components.has(type);
  }
}

export class SDUIRenderer {
  private componentRegistry: ComponentRegistry;

  constructor() {
    this.componentRegistry = new ComponentRegistry();
  }

  // 注册组件
  registerComponent(type: string, component: Component): void {
    this.componentRegistry.register(type, component);
  }

  // 创建渲染组件
  createRenderComponent(config: ComponentConfig): VNode | null {
    const component = this.componentRegistry.get(config.type);
    if (!component) {
      console.warn(`Component type "${config.type}" not found`);
      return null;
    }

    // 处理绑定
    const props = this.processBindings(config);

    // 处理事件
    const events = this.processEvents(config);

    // 处理条件渲染
    if (config.condition) {
      // TODO: 实现条件渲染逻辑
    }

    // 处理子组件
    const children = config.children?.map(child => this.createRenderComponent(child)) || [];

    return h(component, {
      ...props,
      ...events,
      key: config.id
    }, children);
  }

  // 处理数据绑定
  private processBindings(config: ComponentConfig): Record<string, any> {
    const props = { ...config.props };

    if (config.bindings) {
      Object.entries(config.bindings).forEach(([prop, binding]) => {
        // TODO: 实现数据绑定逻辑
        props[prop] = binding.source; // 临时实现，需要完善
      });
    }

    return props;
  }

  // 处理事件绑定
  private processEvents(config: ComponentConfig): Record<string, Function> {
    const events: Record<string, Function> = {};

    if (config.events) {
      Object.entries(config.events).forEach(([event, handlers]) => {
        events[`on${event.charAt(0).toUpperCase()}${event.slice(1)}`] = (...args: any[]) => {
          handlers.forEach(handler => {
            // TODO: 实现事件处理逻辑
            console.log('Event handler:', handler.type, handler.action, args);
          });
        };
      });
    }

    return events;
  }

  // 创建页面渲染组件
  createPageComponent(pageConfig: PageConfig): Component {
    const self = this;
    return defineComponent({
      name: `Page-${pageConfig.pageKey}`,
      setup() {
        return () => {
          const components = pageConfig.components.map(config => 
            self.createRenderComponent(config)
          ).filter((node): node is VNode => node !== null);

          return h('div', { class: 'sdui-page' }, components);
        };
      }
    });
  }
} 