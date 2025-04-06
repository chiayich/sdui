# SDUI 组件使用示例

**日期**: 2024-05-30  
**作者**: 前端团队  
**状态**: 更新版

本文档提供了SDUI组件库中各组件的配置和使用示例，帮助开发人员理解如何在UI配置中使用这些组件。

## 基础组件

### 容器组件 (container)

容器组件用于包含和布局其他组件。

```json
{
  "id": "main-container",
  "type": "container",
  "style": {
    "padding": "16px",
    "backgroundColor": "#f5f5f5"
  },
  "properties": {
    "direction": "column"
  },
  "children": [
    // 子组件
  ]
}
```

### 文本组件 (text)

文本组件用于显示静态文本内容。

```json
{
  "id": "welcome-text",
  "type": "text",
  "style": {
    "fontSize": "18px",
    "fontWeight": "bold",
    "marginBottom": "16px"
  },
  "properties": {
    "content": "欢迎使用SDUI框架"
  }
}
```

### 按钮组件 (button)

按钮组件用于触发动作。

```json
{
  "id": "submit-button",
  "type": "button",
  "style": {
    "backgroundColor": "#1890ff",
    "color": "white",
    "padding": "8px 16px"
  },
  "properties": {
    "label": "提交",
    "disabled": false
  },
  "events": {
    "click": {
      "type": "api",
      "url": "/api/submit",
      "method": "POST"
    }
  }
}
```

## 表单组件

### 输入框组件 (input)

输入框组件用于收集用户输入的文本数据。

```json
{
  "id": "username-input",
  "type": "input",
  "style": {
    "width": "100%"
  },
  "properties": {
    "label": "用户名",
    "placeholder": "请输入用户名",
    "type": "text",
    "maxLength": 20,
    "helpText": "输入您的用户名或邮箱",
    "required": true
  },
  "events": {
    "onChange": {
      "type": "state",
      "action": "update",
      "target": "formData.username"
    }
  }
}
```

支持的输入类型：
- `text`: 文本输入框
- `password`: 密码输入框
- `number`: 数字输入框
- `email`: 邮箱输入框
- `tel`: 电话号码输入框

### 选择器组件 (select)

选择器组件用于从预设选项中选择一个或多个选项。

```json
{
  "id": "role-select",
  "type": "select",
  "style": {
    "width": "100%"
  },
  "properties": {
    "label": "角色",
    "placeholder": "请选择角色",
    "options": [
      {"label": "管理员", "value": "admin"},
      {"label": "编辑", "value": "editor"},
      {"label": "访客", "value": "visitor", "disabled": true}
    ],
    "multiple": false,
    "required": true,
    "helpText": "选择用户角色类型"
  },
  "events": {
    "change": {
      "type": "state",
      "action": "update",
      "target": "formData.role"
    }
  }
}
```

选择器组件属性：
- `label`: 标签文本
- `placeholder`: 占位提示文本
- `options`: 选项数组，每个选项包含label和value
- `multiple`: 是否支持多选
- `disabled`: 是否禁用
- `required`: 是否必填
- `hasError`: 是否显示错误状态
- `errorMessage`: 错误提示文本
- `helpText`: 帮助提示文本

### 复选框组件 (checkbox)

复选框组件用于单个布尔值或多选场景。

```json
{
  "id": "terms-checkbox",
  "type": "checkbox",
  "style": {
    "marginTop": "16px"
  },
  "properties": {
    "label": "我已阅读并同意《服务条款》",
    "value": false,
    "required": true,
    "errorMessage": "必须同意服务条款才能继续"
  },
  "events": {
    "change": {
      "type": "state",
      "action": "update",
      "target": "formData.acceptTerms"
    }
  }
}
```

复选框组件属性：
- `label`: 标签文本
- `value`: 是否选中
- `disabled`: 是否禁用
- `required`: 是否必填
- `hasError`: 是否显示错误状态
- `errorMessage`: 错误提示文本
- `helpText`: 帮助提示文本

### 单选框组件 (radio)

单选框组件用于从多个选项中选择一个选项。

```json
{
  "id": "gender-radio",
  "type": "radio",
  "style": {
    "marginBottom": "16px"
  },
  "properties": {
    "label": "性别",
    "options": [
      {"label": "男", "value": "male"},
      {"label": "女", "value": "female"},
      {"label": "其他", "value": "other"}
    ],
    "value": "",
    "vertical": true,
    "required": true,
    "errorMessage": "请选择性别"
  },
  "events": {
    "change": {
      "type": "state",
      "action": "update",
      "target": "formData.gender"
    }
  }
}
```

单选框组件属性：
- `label`: 组标签文本
- `options`: 选项数组，每个选项包含label和value
- `value`: 当前选中的值
- `disabled`: 是否禁用
- `vertical`: 是否垂直排列
- `required`: 是否必填
- `hasError`: 是否显示错误状态
- `errorMessage`: 错误提示文本
- `helpText`: 帮助提示文本

### 开关组件 (switch)

开关组件用于切换布尔状态值。

```json
{
  "id": "notification-switch",
  "type": "switch",
  "style": {
    "marginBottom": "16px"
  },
  "properties": {
    "label": "开启通知",
    "labelPosition": "right",
    "value": true,
    "size": "default",
    "helpText": "接收系统通知和更新"
  },
  "events": {
    "change": {
      "type": "state",
      "action": "update",
      "target": "userPrefs.notifications"
    }
  }
}
```

开关组件属性：
- `label`: 标签文本
- `labelPosition`: 标签位置，可选 "left" 或 "right"
- `value`: 开关状态
- `size`: 大小，可选 "small", "default", "large"
- `disabled`: 是否禁用
- `loading`: 是否显示加载状态
- `required`: 是否必须
- `hasError`: 是否显示错误状态
- `errorMessage`: 错误提示文本
- `helpText`: 帮助提示文本

## 布局组件

### 列表组件 (list)

列表组件用于展示数据列表，支持滚动分页。

```json
{
  "id": "user-list",
  "type": "list",
  "style": {
    "height": "400px",
    "border": "1px solid #ebeef5",
    "borderRadius": "4px"
  },
  "properties": {
    "title": "用户列表",
    "titleField": "name",
    "descriptionField": "email",
    "emptyText": "暂无用户数据",
    "pageSize": 10,
    "static": false
  },
  "events": {
    "onLoadData": {
      "type": "api",
      "url": "/api/users",
      "method": "GET"
    },
    "onItemClick": {
      "type": "navigation",
      "url": "/user/details"
    }
  }
}
```

列表组件属性：
- `title`: 列表标题
- `titleField`: 显示为项目标题的字段名
- `descriptionField`: 显示为项目描述的字段名
- `pageSize`: 每页加载的项目数量
- `static`: 是否使用静态数据
- `emptyText`: 无数据时显示的文本
- `endText`: 全部加载完毕时显示的文本
- `items`: 静态数据项列表

### 表格组件 (table)

表格组件用于展示结构化数据，支持排序和分页。

```json
{
  "id": "product-table",
  "type": "table",
  "style": {
    "width": "100%"
  },
  "properties": {
    "title": "产品列表",
    "columns": [
      {
        "key": "id",
        "title": "ID",
        "width": "80px"
      },
      {
        "key": "name",
        "title": "产品名称",
        "sortable": true
      },
      {
        "key": "price",
        "title": "价格",
        "sortable": true
      },
      {
        "key": "status",
        "title": "状态"
      }
    ],
    "pagination": true,
    "pageSize": 10,
    "showTotal": true,
    "showSizeChanger": true,
    "selectable": true,
    "selectMode": "multiple",
    "rowKey": "id",
    "actions": [
      {
        "text": "查看",
        "type": "primary",
        "key": "view"
      },
      {
        "text": "删除",
        "type": "danger",
        "key": "delete",
        "disabled": (row) => row.status === "locked"
      }
    ]
  },
  "events": {
    "onLoadData": {
      "type": "api",
      "url": "/api/products",
      "method": "GET"
    },
    "onAction": {
      "type": "handler",
      "handler": "handleTableAction"
    }
  }
}
```

表格组件属性：
- `title`: 表格标题
- `columns`: 表格列配置
- `pagination`: 是否启用分页
- `pageSize`: 每页显示条数
- `showTotal`: 是否显示总条数
- `showSizeChanger`: 是否显示页大小选择器
- `selectable`: 是否可选择行
- `selectMode`: 选择模式 (single/multiple)
- `rowKey`: 行唯一标识字段
- `actions`: 行操作按钮配置

### 无限滚动组件 (infiniteScroll)

无限滚动组件提供高性能的滚动加载功能，特别适用于大数据列表。

```json
{
  "id": "news-feed",
  "type": "infiniteScroll",
  "style": {
    "height": "500px"
  },
  "properties": {
    "threshold": 200,
    "useObserver": true,
    "loadingText": "正在加载更多...",
    "endText": "没有更多内容了",
    "errorText": "加载失败",
    "retryText": "点击重试"
  },
  "events": {
    "onLoadMore": {
      "type": "api",
      "url": "/api/news-feed",
      "method": "GET"
    }
  },
  "children": [
    {
      "id": "feed-container",
      "type": "container",
      "children": [
        // 动态生成的内容项
      ]
    }
  ]
}
```

无限滚动组件属性：
- `threshold`: 触发加载的阈值（距离底部多少像素开始加载）
- `useObserver`: 是否使用 IntersectionObserver（提高性能）
- `loadingText`: 加载中显示的文本
- `endText`: 全部加载完时显示的文本
- `errorText`: 加载失败时显示的文本
- `retryText`: 重试按钮文本
- `maxPage`: 最大页数限制

### 栅格行组件 (row)

栅格行组件是栅格布局系统的行容器，用于水平布局多个列组件。

```json
{
  "id": "form-row",
  "type": "row",
  "style": {
    "marginBottom": "16px"
  },
  "properties": {
    "gutter": 16,
    "justify": "space-between",
    "align": "middle",
    "wrap": true
  },
  "children": [
    // 列组件
  ]
}
```

栅格行组件属性：
- `gutter`: 列间距（像素）
- `justify`: 水平对齐方式，可选 "flex-start", "flex-end", "center", "space-between", "space-around"
- `align`: 垂直对齐方式，可选 "flex-start", "flex-end", "center", "stretch"
- `wrap`: 是否换行

### 栅格列组件 (col)

栅格列组件是栅格布局系统的列容器，用于在行内垂直布局组件。

```json
{
  "id": "name-col",
  "type": "col",
  "properties": {
    "span": 12,
    "offset": 0,
    "xs": 24,
    "sm": 12,
    "md": 8,
    "lg": 6
  },
  "children": [
    // 子组件
  ]
}
```

栅格列组件属性：
- `span`: 列宽度，占据的栅格数（1-24）
- `offset`: 左侧偏移栅格数
- `xs`: <576px 响应式栅格
- `sm`: ≥576px 响应式栅格
- `md`: ≥768px 响应式栅格
- `lg`: ≥992px 响应式栅格
- `xl`: ≥1200px 响应式栅格

### 卡片组件 (card)

卡片组件用于将信息进行分组展示，有标题、内容和页脚区域。

```json
{
  "id": "stats-card",
  "type": "card",
  "style": {
    "marginBottom": "24px",
    "width": "100%"
  },
  "properties": {
    "title": "统计数据",
    "extra": "更多",
    "bordered": true,
    "hoverable": true,
    "size": "default",
    "footer": "更新于 2024-05-30"
  },
  "children": [
    // 子组件
  ]
}
```

卡片组件属性：
- `title`: 卡片标题
- `extra`: 卡片右上角的额外内容
- `bordered`: 是否有边框
- `hoverable`: 鼠标悬浮时是否有阴影效果
- `bodyPadding`: 内容区域的内边距
- `size`: 卡片大小，可选 "small", "default", "large"
- `footer`: 卡片底部内容

### 分割线组件 (divider)

分割线组件用于分割不同内容的区域。

```json
{
  "id": "section-divider",
  "type": "divider",
  "style": {
    "margin": "32px 0"
  },
  "properties": {
    "vertical": false,
    "dashed": false,
    "text": "第二部分",
    "orientation": "center"
  }
}
```

分割线组件属性：
- `vertical`: 是否为垂直分割线
- `dashed`: 是否为虚线
- `text`: 分割线中的文本
- `orientation`: 文本位置，可选 "left", "center", "right"

## 组件组合示例

### 表单布局示例

以下是使用栅格和表单组件构建的表单布局：

```json
{
  "id": "registration-form",
  "type": "container",
  "children": [
    {
      "id": "form-title",
      "type": "text",
      "properties": {
        "content": "用户注册"
      },
      "style": {
        "fontSize": "24px",
        "fontWeight": "bold",
        "marginBottom": "24px"
      }
    },
    {
      "id": "form-card",
      "type": "card",
      "properties": {
        "bordered": true
      },
      "children": [
        {
          "id": "basic-info-row",
          "type": "row",
          "properties": {
            "gutter": 16
          },
          "children": [
            {
              "id": "username-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "username-input",
                  "type": "input",
                  "properties": {
                    "label": "用户名",
                    "placeholder": "请输入用户名",
                    "required": true
                  }
                }
              ]
            },
            {
              "id": "password-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "password-input",
                  "type": "input",
                  "properties": {
                    "label": "密码",
                    "placeholder": "请输入密码",
                    "type": "password",
                    "required": true
                  }
                }
              ]
            }
          ]
        },
        {
          "id": "contact-row",
          "type": "row",
          "properties": {
            "gutter": 16
          },
          "children": [
            {
              "id": "email-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "email-input",
                  "type": "input",
                  "properties": {
                    "label": "邮箱",
                    "placeholder": "请输入邮箱",
                    "type": "email",
                    "required": true
                  }
                }
              ]
            },
            {
              "id": "phone-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "phone-input",
                  "type": "input",
                  "properties": {
                    "label": "手机号",
                    "placeholder": "请输入手机号",
                    "type": "tel"
                  }
                }
              ]
            }
          ]
        },
        {
          "id": "role-row",
          "type": "row",
          "children": [
            {
              "id": "role-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "role-select",
                  "type": "select",
                  "properties": {
                    "label": "角色",
                    "placeholder": "请选择角色",
                    "options": [
                      {"label": "管理员", "value": "admin"},
                      {"label": "编辑", "value": "editor"},
                      {"label": "用户", "value": "user"}
                    ]
                  }
                }
              ]
            },
            {
              "id": "gender-col",
              "type": "col",
              "properties": {
                "span": 12
              },
              "children": [
                {
                  "id": "gender-radio",
                  "type": "radio",
                  "properties": {
                    "label": "性别",
                    "options": [
                      {"label": "男", "value": "male"},
                      {"label": "女", "value": "female"}
                    ]
                  }
                }
              ]
            }
          ]
        },
        {
          "id": "preferences-section",
          "type": "container",
          "children": [
            {
              "id": "preferences-divider",
              "type": "divider",
              "properties": {
                "text": "偏好设置",
                "orientation": "left"
              }
            },
            {
              "id": "newsletter-row",
              "type": "row",
              "children": [
                {
                  "id": "newsletter-col",
                  "type": "col",
                  "properties": {
                    "span": 12
                  },
                  "children": [
                    {
                      "id": "newsletter-checkbox",
                      "type": "checkbox",
                      "properties": {
                        "label": "订阅新闻通讯"
                      }
                    }
                  ]
                },
                {
                  "id": "notification-col",
                  "type": "col",
                  "properties": {
                    "span": 12
                  },
                  "children": [
                    {
                      "id": "notification-switch",
                      "type": "switch",
                      "properties": {
                        "label": "启用通知",
                        "value": true
                      }
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          "id": "terms-container",
          "type": "container",
          "style": {
            "marginTop": "24px"
          },
          "children": [
            {
              "id": "terms-checkbox",
              "type": "checkbox",
              "properties": {
                "label": "我已阅读并同意《服务条款》和《隐私政策》",
                "required": true
              }
            }
          ]
        },
        {
          "id": "buttons-row",
          "type": "row",
          "style": {
            "marginTop": "24px"
          },
          "properties": {
            "justify": "flex-end",
            "gutter": 16
          },
          "children": [
            {
              "id": "cancel-col",
              "type": "col",
              "children": [
                {
                  "id": "cancel-button",
                  "type": "button",
                  "properties": {
                    "label": "取消"
                  }
                }
              ]
            },
            {
              "id": "submit-col",
              "type": "col",
              "children": [
                {
                  "id": "submit-button",
                  "type": "button",
                  "properties": {
                    "label": "注册"
                  },
                  "style": {
                    "backgroundColor": "#1890ff",
                    "color": "white"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

## 事件处理

组件可以通过 `events` 属性定义事件处理逻辑。支持的事件类型：

1. **API调用**：触发后端API请求
   ```json
   "events": {
     "click": {
       "type": "api",
       "url": "/api/endpoint",
       "method": "POST",
       "data": "{{formData}}"
     }
   }
   ```

2. **导航**：页面跳转
   ```json
   "events": {
     "click": {
       "type": "navigation",
       "url": "/target-page"
     }
   }
   ```

3. **状态更新**：更新UI状态
   ```json
   "events": {
     "onChange": {
       "type": "state",
       "action": "update",
       "target": "formData.username"
     }
   }
   ```

4. **自定义处理器**：执行特定逻辑
   ```json
   "events": {
     "onChange": {
       "type": "handler",
       "handler": "customHandler"
     }
   }
   ```

## 数据绑定

组件可以通过绑定表达式绑定到状态数据，表达式使用双大括号语法：

```json
{
  "id": "welcome-message",
  "type": "text",
  "properties": {
    "content": "欢迎，{{userData.name}}!"
  }
}
```

## 条件渲染

使用 `visible` 属性可以实现条件渲染：

```json
{
  "id": "error-message",
  "type": "text",
  "properties": {
    "content": "验证失败！"
  },
  "style": {
    "color": "red"
  },
  "visible": "{{formState.hasError}}"
}
``` 