import { PageConfig } from '@/core/types/page';

export const mockProductFlowConfig: PageConfig = {
  pageKey: 'productFlow',
  version: '1.0',
  title: '商品流通工作台',
  layout: {
    type: 'standard',
    header: {
      title: '商品流通工作台',
      breadcrumb: true
    }
  },
  state: {
    searchForm: {
      type: 'object',
      default: {
        store: '',
        dateRange: [],
        status: ''
      }
    },
    tableData: {
      type: 'array',
      default: []
    }
  },
  dataSources: {
    storeList: {
      type: 'api',
      api: '/api/stores',
      method: 'GET',
      cache: {
        enabled: true,
        duration: 3600
      }
    },
    flowList: {
      type: 'api',
      api: '/api/product/flow',
      method: 'GET',
      params: {
        store: '#{state.searchForm.store}',
        dateRange: '#{state.searchForm.dateRange}',
        status: '#{state.searchForm.status}'
      }
    }
  },
  components: [
    {
      type: 'filterBar',
      id: 'searchForm',
      props: {
        items: [
          {
            type: 'select',
            props: {
              label: 'DAZZLE',
              placeholder: '请选择',
              style: { width: '200px' }
            },
            bindings: {
              options: {
                type: 'dataSource',
                source: 'storeList'
              },
              value: {
                type: 'state',
                source: 'searchForm.store'
              }
            }
          },
          {
            type: 'dateRangePicker',
            props: {
              label: '开始日期 ~ 截至日期',
              style: { width: '300px' }
            },
            bindings: {
              value: {
                type: 'state',
                source: 'searchForm.dateRange'
              }
            }
          },
          {
            type: 'select',
            props: {
              label: '执行状态',
              placeholder: '请选择',
              style: { width: '150px' }
            },
            bindings: {
              value: {
                type: 'state',
                source: 'searchForm.status'
              }
            }
          }
        ],
        actions: [
          {
            type: 'button',
            text: '查询',
            props: {
              type: 'primary'
            },
            events: {
              click: [
                {
                  type: 'api',
                  action: 'refreshTable'
                }
              ]
            }
          },
          {
            type: 'button',
            text: '重置',
            events: {
              click: [
                {
                  type: 'state',
                  action: 'resetForm'
                }
              ]
            }
          }
        ]
      }
    },
    {
      type: 'table',
      id: 'mainTable',
      props: {
        columns: [
          {
            title: '需求单号',
            dataIndex: 'orderNo',
            width: 180
          },
          {
            title: '执行状态',
            dataIndex: 'status',
            width: 120
          },
          {
            title: '调出区域',
            dataIndex: 'fromArea',
            width: 150
          },
          {
            title: '调出方',
            dataIndex: 'fromStore',
            width: 200
          },
          {
            title: '调入方',
            dataIndex: 'toStore',
            width: 200
          }
        ],
        pagination: {
          pageSize: 10,
          showTotal: true
        }
      },
      bindings: {
        dataSource: {
          type: 'dataSource',
          source: 'flowList'
        }
      }
    }
  ]
}; 