import { PageConfig } from '@/core/types/page';

export const mockHomeConfig: PageConfig = {
  pageKey: 'instruction',
  version: '1.0',
  title: '流通指令',
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
              title: '流通指令',
              active: true
            },
            {
              key: 'simulation',
              title: '仿真评估'
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
      type: 'filterBar',
      id: 'mainFilter',
      props: {
        items: [
          
          {
            type: 'select',
            id: 'flowType',
            props: {
              placeholder: '宝胜阿迪达斯-调出方视角',
              style: { width: '200px' },
              options: [
                { value: 'option1', label: '宝胜阿迪达斯-调出方视角-调出方排序' },
                { value: 'option2', label: '竖版导出模板' },
                { value: 'option3', label: '宝胜阿迪达斯-调出方主视角' },
                { value: 'option4', label: '宝胜阿迪达斯-调入方主视角' },
                { value: 'option5', label: '系统默认配置' }
              ],
              defaultValue: 'option1'
            }
          },
          {
            type: 'datePicker',
            id: 'flowDate',
            props: {
              placeholder: '请选择日期',
              value: '2025-04-03',
              style: { width: '150px' }
            },
            bindings: {
              value: {
                type: 'state',
                source: 'searchForm.flowDate'
              }
            }
          },
          {
            type: 'select',
            id: 'bizType',
            props: {
              placeholder: '业务动作类型',
              style: { width: '150px' },
              options: [
                { value: 'daily', label: '日常补货' },
                { value: 'rolling', label: '滚动铺货' },
                { value: 'expansion', label: '扩铺' },
                { value: 'collection', label: '集货' },
                { value: 'reorder', label: '翻单' },
                { value: 'storeChange', label: '换店' },
                { value: 'return', label: '返仓' }
              ]
            }
          },
          {
            type: 'select',
            id: 'brand',
            props: {
              placeholder: '品牌',
              style: { width: '150px' },
              options: [
                { value: 'kids', label: 'ADIDAS KIDS(阿迪小童)' },
                { value: 'originals', label: 'ADIDAS ORIGINALS(阿迪经典)' },
                { value: 'sc', label: 'ADIDAS SC(阿迪运动休闲)' },
                { value: 'hw', label: 'ADIDAS HW(阿迪箱包)' },
                { value: 'adidas', label: 'ADIDAS(阿迪)' },
                { value: 'outdoor', label: 'ADIDAS OUTDOOR(阿迪户外)' },
                { value: 'taekwondo', label: 'ADIDAS TAEKWONDO (阿迪达斯跆拳道)' }
              ]
            }
          },
          {
            type: 'select',
            id: 'goodsType',
            props: {
              placeholder: '商品季节',
              style: { width: '150px' },
              options: [
                { value: '2025Q2', label: '2025Q2' },
                { value: '2025Q1', label: '2025Q1' },
                { value: '2024Q4', label: '2024Q4' },
                { value: '2024Q3', label: '2024Q3' },
                { value: '2024Q2', label: '2024Q2' },
                { value: '2024Q1', label: '2024Q1' },
                { value: '2023Q4', label: '2023Q4' }
              ]
            }
          }
        ],
        actions: [
          {
            type: 'button',
            id: 'searchBtn',
            text: '查询',
            props: {
              type: 'primary'
            }
          },
          {
            type: 'button',
            id: 'resetBtn',
            text: '重置'
          },
          {
            type: 'button',
            id: 'expandBtn',
            text: '展开',
            props: {
              type: 'link'
            }
          }
        ]
      }
    },
    {
      type: 'toolbar',
      id: 'tableToolbar',
      props: {
        items: [
          {
            type: 'selection',
            id: 'selectAll',
            text: 'SKC',
            props: {
              options: ['启用多选']
            }
          }
        ],
        actions: [
          {
            type: 'button',
            id: 'saveBtn',
            text: '保存',
            props: {
              type: 'primary'
            }
          },
          {
            type: 'button',
            id: 'exportBtn',
            text: '导出...'
          },
          {
            type: 'button',
            id: 'importBtn',
            text: '导入'
          },
          {
            type: 'button',
            id: 'clearBtn',
            text: '清空'
          },
          {
            type: 'button',
            id: 'viewBtn',
            icon: 'view',
            props: {
              shape: 'square'
            }
          }
        ]
      }
    },
    {
      type: 'imageList',
      id: 'productImages',
      props: {
        items: [
          { id: 'IF1809W', selected: true, highlight: false },
          { id: 'JC9268', selected: false, highlight: true },
          { id: 'JC9269', selected: false, highlight: true },
          { id: 'JM8009', selected: false, highlight: true },
          { id: 'JC9286', selected: false, highlight: false },
          { id: 'B75806W', selected: false, highlight: false },
          { id: 'JY8561', selected: false, highlight: true },
          { id: 'IH8659W', selected: false, highlight: true },
          { id: 'IT3981', selected: false, highlight: true },
          { id: 'IA4850', selected: false, highlight: false },
          { id: 'JR0035', selected: false, highlight: false },
          { id: 'JY8563', selected: false, highlight: false },
          { id: 'JC8371', selected: false, highlight: false },
          { id: 'JI0079W', selected: false, highlight: false }
        ],
        style: {
          marginBottom: '16px'
        }
      }
    },
    {
      type: 'table',
      id: 'flowTable',
      props: {
        columns: [
          {
            title: '',
            dataIndex: 'select',
            width: 40,
            align: 'center'
          },
          {
            title: '行号',
            dataIndex: 'lineNo',
            width: 60,
            align: 'center'
          },
          {
            title: '业务动作',
            dataIndex: 'bizAction',
            width: 100
          },
          {
            title: '动作模板',
            dataIndex: 'actionTemplate',
            width: 100
          },
          {
            title: '异常类型',
            dataIndex: 'exceptionType',
            width: 100
          },
          {
            title: '调出区域',
            dataIndex: 'outRegion',
            width: 100
          },
          {
            title: '调出方',
            dataIndex: 'outStore',
            width: 200
          },
          {
            title: '当季首调日期',
            dataIndex: 'firstDate',
            width: 120,
            align: 'center'
          },
          {
            title: '调出方模板补调后库存',
            dataIndex: 'outStockAfter',
            width: 100,
            align: 'right',
            className: 'highlighted-column'
          },
          {
            title: '调出方模板补后库存',
            dataIndex: 'outStock',
            width: 100,
            align: 'right',
            className: 'highlighted-column'
          }
        ],
        dataSource: [
          {
            key: '1',
            lineNo: 1,
            bizAction: '日常补货',
            actionTemplate: '浙江-补货',
            outRegion: '浙江区部',
            outStore: '宝胜金华通道中心仓',
            firstDate: '2025-03-17',
            outStockAfter: 415,
            outStock: 401
          },
          {
            key: '2',
            lineNo: 2,
            bizAction: '日常补货',
            actionTemplate: '浙江-补货',
            outRegion: '浙江区部',
            outStore: '宝胜金华通道北仓',
            firstDate: '2025-03-16',
            outStockAfter: 544,
            outStock: 515
          },
          {
            key: '3',
            lineNo: 3,
            bizAction: '日常补货',
            actionTemplate: '浙江-补货',
            outRegion: '浙江区部',
            outStore: '宝胜金华通道中心仓',
            firstDate: '2025-03-17',
            outStockAfter: 415,
            outStock: 401
          },
          {
            key: '4',
            lineNo: 4,
            bizAction: '日常补货',
            actionTemplate: '浙江-补货',
            outRegion: '浙江区部',
            outStore: '宝胜金华通道北仓',
            firstDate: '2025-03-16',
            outStockAfter: 544,
            outStock: 515
          },
          {
            key: '5',
            lineNo: 5,
            bizAction: '日常补货',
            actionTemplate: '浙江-补货',
            outRegion: '浙江区部',
            outStore: '宝胜金华通道中心仓',
            firstDate: '2025-03-17',
            outStockAfter: 415,
            outStock: 401
          }
        ],
        pagination: {
          pageSize: 10,
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
      default: 'instruction'
    },
    flowType: {
      type: 'string',
      default: ''
    },
    flowDate: {
      type: 'string',
      default: '2025-04-03'
    },
    bizType: {
      type: 'string',
      default: ''
    }
  }
}; 