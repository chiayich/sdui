import { AppConfig } from '@/core/types/framework';

export const mockAppConfig: AppConfig = {
  layout: {
    header: {
      height: 64,
      fixed: true,
      components: {
        logo: {
          src: '/logo.png',
          alt: '商品通',
          width: 120,
          height: 32
        },
        userInfo: {
          avatar: '/avatar.png',
          name: 'admin',
          role: '超级管理员'
        },
        globalSearch: {
          placeholder: '搜索...',
          width: 200
        }
      }
    },
    sider: {
      width: 200,
      collapsible: true,
      theme: 'dark'
    },
    content: {
      padding: 24,
      tabMode: 'multi'
    }
  },
  router: {
    mode: 'history',
    routes: [
      {
        id: 'product',
        path: '/product',
        pageKey: 'product',
        title: '商品通',
        icon: 'ShoppingOutlined',
        children: [
          {
            id: 'product-flow',
            path: '/product/flow',
            pageKey: 'productFlow',
            title: '商品流通工作台'
          },
          {
            id: 'product-plan',
            path: '/product/plan',
            pageKey: 'productPlan',
            title: '商品计划'
          }
        ]
      },
      {
        id: 'enterprise',
        path: '/enterprise',
        pageKey: 'enterprise',
        title: '企业洞察',
        icon: 'BarChartOutlined'
      },
      {
        id: 'otb',
        path: '/otb',
        pageKey: 'otb',
        title: 'OTB',
        icon: 'FundOutlined'
      }
    ]
  },
  state: {
    persist: true,
    defaultState: {
      theme: 'light',
      locale: 'zh-CN'
    }
  }
}; 