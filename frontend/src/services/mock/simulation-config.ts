import { PageConfig } from '@/core/types/page';

export const mockSimulationConfig: PageConfig = {
  pageKey: 'simulation',
  version: '1.0',
  title: '仿真评估',
  layout: {
    type: 'admin',
    header: {
      title: '商品通',
      logo: '/static/logos/logo.png',
      userInfo: {
        name: 'baosheng',
        role: '超级管理员'
      },
      style: {
        background: '#001529',
        color: '#fff',
        padding: '0 24px',
        height: '48px',
        boxShadow: '0 1px 4px rgba(0,21,41,.08)'
      }
    },
    sider: {
      width: 200,
      theme: 'dark',
      menu: [
        {
          key: 'flow',
          icon: 'shopping-cart',
          title: '商品流通',
          children: [
            {
              key: 'workbench',
              title: '商品流通工作台'
            },
            {
              key: 'collection',
              title: '集货'
            },
            {
              key: 'instruction',
              title: '流通指令'
            },
            {
              key: 'simulation',
              title: '仿真评估',
              active: true
            },
            {
              key: 'overview',
              title: '门店概览'
            }
          ]
        },
        {
          key: 'system',
          icon: 'setting',
          title: '系统配置'
        }
      ]
    }
  },
  components: [
    {
      type: 'tabs',
      id: 'mainTabs',
      props: {
        activeKey: 'system',
        items: [
          {
            key: 'system',
            label: '系统'
          },
          {
            key: 'detail',
            label: '明细核查'
          }
        ],
        style: {
          marginBottom: '20px'
        }
      }
    },
    {
      type: 'filterBar',
      id: 'filterTags',
      props: {
        items: [
          {
            type: 'tags',
            id: 'selectedTags',
            props: {
              label: '已选条件：',
              tags: [
                { id: 'tag1', text: '浙江区部', closable: true },
                { id: 'tag2', text: '浙江-补货', closable: true },
                { id: 'tag3', text: '浙江区部', closable: true },
                { id: 'tag4', text: '浙北区域', closable: true },
                { id: 'tag5', text: '浙中区域', closable: true }
              ]
            }
          }
        ]
      }
    },
    {
      type: 'filterBar',
      id: 'conditionFilter',
      props: {
        items: [
          {
            type: 'dropdown',
            id: 'normalFlow',
            props: {
              placeholder: '常用筛选',
              icon: 'down',
              style: { width: '120px' }
            }
          },
          {
            type: 'dropdown',
            id: 'storeFlow',
            props: {
              placeholder: '门店筛选',
              icon: 'down',
              style: { width: '120px' }
            }
          },
          {
            type: 'dropdown',
            id: 'productFlow',
            props: {
              placeholder: '商品筛选',
              icon: 'down',
              style: { width: '120px' }
            }
          }
        ],
        actions: [
          {
            type: 'button',
            id: 'saveFilter',
            text: '保存为默认查询',
            props: {
              type: 'default'
            }
          },
          {
            type: 'button',
            id: 'resetBtn',
            text: '重置'
          },
          {
            type: 'button',
            id: 'searchBtn',
            text: '查询',
            props: {
              type: 'primary'
            }
          }
        ]
      }
    },
    {
      type: 'row',
      id: 'statsRow',
      props: {
        gutter: 16,
        children: [
          {
            type: 'card',
            id: 'totalQuantityCard',
            props: {
              title: '补调入数量',
              value: '842件',
              footer: '调出量 0件',
              style: {
                width: '25%'
              }
            }
          },
          {
            type: 'card',
            id: 'totalStoreCard',
            props: {
              title: '补调入包数',
              value: '63个',
              footer: '调出包数 —',
              style: {
                width: '25%'
              }
            }
          },
          {
            type: 'card',
            id: 'disruptionRateCard',
            props: {
              title: '补调后断码率',
              value: '11.5%',
              footer: '补调前 11.7% ▼ 0.2%',
              trend: 'down',
              style: {
                width: '25%'
              }
            }
          },
          {
            type: 'card',
            id: 'targetSatisfactionCard',
            props: {
              title: '目标库存满足率',
              value: '74.2%',
              footer: '补调前 73% ▲ 1.2%',
              trend: 'up',
              style: {
                width: '25%'
              }
            }
          }
        ]
      }
    },
    {
      type: 'row',
      id: 'statsRow2',
      props: {
        gutter: 16,
        children: [
          {
            type: 'card',
            id: 'turnoverDaysCard',
            props: {
              title: '周转天数 (店均)',
              value: '303.8天',
              footer: '补调前 303.1天 ▲ 0.7天',
              trend: 'up',
              style: {
                width: '25%'
              }
            }
          },
          {
            type: 'card',
            id: 'activeRateCard',
            props: {
              title: '动销率',
              value: '30.6%',
              footer: '补调前 30.6% — 0%',
              style: {
                width: '25%'
              }
            }
          },
          {
            type: 'card',
            id: 'storeDistributionCard',
            props: {
              title: '门店分布-净补调入量',
              chart: 'barChart',
              chartData: [
                { category: '<-9', value: 8 },
                { category: '-9', value: 13 },
                { category: '-5', value: 12 },
                { category: '-1', value: 17 },
                { category: '-0', value: 4 },
                { category: '<5', value: 1 },
                { category: '<9', value: 3 },
                { category: '<13', value: 1 },
                { category: '<17', value: 3 },
                { category: '>17', value: 1 }
              ],
              style: {
                width: '50%',
                height: '200px'
              }
            }
          }
        ]
      }
    },
    {
      type: 'toolbar',
      id: 'tableToolbar',
      props: {
        title: '明细核查',
        actions: [
          {
            type: 'button',
            id: 'netInBtn',
            text: '净补调入量',
            props: {
              type: 'primary'
            }
          },
          {
            type: 'button',
            id: 'outBtn',
            text: '调出量'
          }
        ]
      }
    },
    {
      type: 'table',
      id: 'detailTable',
      props: {
        columns: [
          {
            title: '序号',
            dataIndex: 'id',
            width: 60,
            align: 'center'
          },
          {
            title: '城市',
            dataIndex: 'city',
            width: 100
          },
          {
            title: '门店编码',
            dataIndex: 'storeCode',
            width: 120
          },
          {
            title: '门店名称',
            dataIndex: 'storeName',
            width: 200
          },
          {
            title: '库存量',
            dataIndex: 'inventory',
            width: 100,
            align: 'right'
          },
          {
            title: '近14天销量',
            dataIndex: 'sales14d',
            width: 120,
            align: 'right'
          },
          {
            title: '近7天销量',
            dataIndex: 'sales7d',
            width: 120,
            align: 'right'
          },
          {
            title: '补调入量',
            dataIndex: 'inQuantity',
            width: 100,
            align: 'right'
          },
          {
            title: '调出量',
            dataIndex: 'outQuantity',
            width: 100,
            align: 'right'
          },
          {
            title: '净补调入量',
            dataIndex: 'netInQuantity',
            width: 100,
            align: 'right'
          }
        ],
        dataSource: [
          {
            id: 1,
            city: '金华市',
            storeCode: 'SP003315',
            storeName: '金华永盛购物中心北门...',
            inventory: 5982,
            sales14d: 164,
            sales7d: 75,
            inQuantity: 5,
            outQuantity: 0,
            netInQuantity: 5
          },
          {
            id: 2,
            city: '杭州市',
            storeCode: 'SP005239',
            storeName: '杭州余杭万达广场AC',
            inventory: 1099,
            sales14d: 46,
            sales7d: 17,
            inQuantity: 5,
            outQuantity: 0,
            netInQuantity: 5
          },
          {
            id: 3,
            city: '绍兴市',
            storeCode: 'SP006409',
            storeName: '上虞万达广场AD',
            inventory: 1808,
            sales14d: 85,
            sales7d: 37,
            inQuantity: 5,
            outQuantity: 0,
            netInQuantity: 5
          }
        ],
        pagination: {
          pageSize: 10,
          total: 63,
          showTotal: true
        },
        style: {
          background: '#fff'
        }
      }
    }
  ],
  state: {
    currentMenu: {
      type: 'string',
      default: 'simulation'
    },
    activeTab: {
      type: 'string',
      default: 'system'
    }
  }
}; 