# 组织架构与权限系统

**日期**: 2024-06-05
**类别**: 系统设计
**状态**: 实施中

## 设计目标

设计并实现一个灵活的组织架构和权限管理系统，以支持多层级组织结构和基于角色的权限控制，同时与SDUI架构无缝集成。

## 系统架构

### 数据模型

1. **组织节点 (OrganizationNode)**:
   - 支持多级树状结构
   - 每个节点有类型区分（根节点、大区、小区、门店等）
   - 通过路径字段快速查询节点层级关系

2. **角色 (Role)**:
   - 定义用户角色（如管理员、运营、财务等）
   - 与权限和组织节点关联
   - 支持系统角色和自定义角色

3. **权限 (Permission)**:
   - 定义系统功能权限
   - 按模块和类型分类
   - 支持页面访问、操作执行等权限类型

4. **用户 (User)**:
   - 基本用户信息
   - 与角色多对多关联
   - 关联主要组织节点

### 权限控制机制

1. **功能权限**:
   - 通过角色-权限关联控制用户可访问的功能
   - 支持权限树形展示和管理
   - 细粒度到具体操作按钮的显示控制

2. **数据权限**:
   - 通过角色-组织节点关联控制数据访问范围
   - 支持全部数据和自定义数据两种模式
   - 可设置是否包含子节点数据

## 前端实现 (SDUI方式)

采用SDUI（Server-Driven UI）方式实现前端界面，由后端提供UI配置数据，前端负责渲染。

### SDUI实现步骤

1. **定义UI Schema**:
   - 组织树组件schema
   - 表单组件schema
   - 列表/表格组件schema

2. **端点设计**:
   - `/api/sdui/system/organization` - 组织管理页面配置
   - `/api/sdui/system/role` - 角色管理页面配置
   - `/api/sdui/system/permission` - 权限配置页面配置

3. **数据交互**:
   - 使用统一的API调用机制
   - 事件处理通过事件映射表实现

### 组织管理页面 UI Schema 示例

```json
{
  "type": "page",
  "id": "organizationManagementPage",
  "title": "组织架构管理",
  "layout": {
    "type": "splitPane",
    "leftWidth": "30%",
    "rightWidth": "70%",
    "left": {
      "type": "card",
      "title": "组织架构树",
      "content": {
        "type": "tree",
        "id": "orgTree",
        "dataSource": "api://organization/tree",
        "props": {
          "nodeKey": "id",
          "labelKey": "name",
          "defaultExpandAll": true
        },
        "events": {
          "nodeClick": "handleNodeClick"
        },
        "actions": [
          {
            "type": "button",
            "text": "添加根节点",
            "permission": "organization:add",
            "props": {
              "type": "primary",
              "size": "small"
            },
            "events": {
              "click": "handleAddRoot"
            }
          }
        ]
      }
    },
    "right": {
      "type": "card",
      "title": "节点详情",
      "content": {
        "type": "dynamicContent",
        "id": "nodeDetail",
        "loading": "{{loading}}",
        "emptyText": "请从左侧选择一个组织节点",
        "content": {
          "type": "container",
          "visible": "{{!!selectedNode}}",
          "children": [
            {
              "type": "descriptions",
              "title": "基本信息",
              "items": [
                { "label": "节点ID", "value": "{{selectedNode.id}}" },
                { "label": "节点名称", "value": "{{selectedNode.name}}" },
                { "label": "节点编码", "value": "{{selectedNode.code}}" },
                { "label": "节点类型", "value": "{{selectedNode.node_type}}" },
                { "label": "路径", "value": "{{selectedNode.path}}" }
              ]
            },
            {
              "type": "table",
              "title": "子节点列表",
              "visible": "{{selectedNode.children && selectedNode.children.length > 0}}",
              "dataSource": "{{selectedNode.children}}",
              "columns": [
                { "title": "名称", "dataIndex": "name" },
                { "title": "编码", "dataIndex": "code" },
                { "title": "类型", "dataIndex": "node_type" },
                {
                  "title": "操作",
                  "actions": [
                    {
                      "type": "button",
                      "text": "查看",
                      "props": { "type": "primary", "size": "small" },
                      "events": { "click": "handleViewChild" }
                    },
                    {
                      "type": "button",
                      "text": "编辑",
                      "permission": "organization:edit",
                      "props": { "type": "info", "size": "small" },
                      "events": { "click": "handleEditChild" }
                    }
                  ]
                }
              ]
            }
          ]
        },
        "actions": [
          {
            "type": "button",
            "text": "添加子节点",
            "permission": "organization:add",
            "visible": "{{canAddChild}}",
            "props": { "type": "primary", "size": "small" },
            "events": { "click": "handleAddChild" }
          },
          {
            "type": "button",
            "text": "编辑节点",
            "permission": "organization:edit",
            "visible": "{{!!selectedNode}}",
            "props": { "type": "info", "size": "small" },
            "events": { "click": "handleEdit" }
          },
          {
            "type": "button",
            "text": "删除节点",
            "permission": "organization:delete",
            "visible": "{{canDelete}}",
            "props": { "type": "danger", "size": "small" },
            "events": { "click": "handleDelete" }
          }
        ]
      }
    }
  },
  "dialogs": [
    {
      "id": "nodeFormDialog",
      "title": "{{dialogType === 'add' ? '添加节点' : '编辑节点'}}",
      "visible": "{{dialogVisible}}",
      "width": "500px",
      "content": {
        "type": "form",
        "id": "nodeForm",
        "model": "{{form}}",
        "labelWidth": "120px",
        "items": [
          {
            "type": "input",
            "label": "节点名称",
            "prop": "name",
            "rules": [
              { "required": true, "message": "请输入节点名称" },
              { "min": 2, "max": 50, "message": "长度在2到50个字符" }
            ]
          },
          {
            "type": "input",
            "label": "节点编码",
            "prop": "code",
            "rules": [
              { "required": true, "message": "请输入节点编码" },
              { "pattern": "^[a-zA-Z0-9_]+$", "message": "编码只能包含字母、数字和下划线" }
            ]
          },
          {
            "type": "select",
            "label": "节点类型",
            "prop": "node_type",
            "options": "{{getAvailableNodeTypes()}}",
            "rules": [{ "required": true, "message": "请选择节点类型" }]
          },
          {
            "type": "inputNumber",
            "label": "排序号",
            "prop": "sort_order",
            "props": { "min": 0, "max": 9999 }
          },
          {
            "type": "switch",
            "label": "是否启用",
            "prop": "is_active"
          }
        ]
      },
      "footer": {
        "cancelText": "取消",
        "confirmText": "确定",
        "confirmLoading": "{{submitLoading}}",
        "onCancel": "handleCancel",
        "onConfirm": "submitForm"
      }
    }
  ]
}
```

## 后端实现

### 模型结构

已实现以下数据模型：
- OrganizationNode
- Role
- Permission
- RoleOrgPermission
- User

### API端点

1. **组织管理**:
   - GET `/api/organization/tree` - 获取组织树
   - GET `/api/organization/node/{node_id}` - 获取单个节点详情
   - POST `/api/organization/node` - 创建节点
   - PUT `/api/organization/node/{node_id}` - 更新节点
   - DELETE `/api/organization/node/{node_id}` - 删除节点

2. **角色管理**:
   - GET `/api/roles` - 获取角色列表
   - POST `/api/roles` - 创建角色
   - PUT `/api/roles/{role_id}` - 更新角色
   - DELETE `/api/roles/{role_id}` - 删除角色

3. **权限管理**:
   - GET `/api/permissions` - 获取所有权限
   - GET `/api/permissions/tree` - 获取权限树
   - GET `/api/roles/{role_id}/permissions` - 获取角色权限
   - POST `/api/roles/{role_id}/permissions` - 更新角色权限

4. **组织权限**:
   - GET `/api/roles/{role_id}/org-permissions` - 获取角色组织权限
   - POST `/api/roles/{role_id}/org-permissions` - 更新角色组织权限

5. **权限检查**:
   - GET `/api/check-permission/{permission_code}` - 检查用户是否有特定权限
   - GET `/api/user-accessible-orgs` - 获取用户可访问的组织节点

### SDUI端点实现（待开发）

为实现SDUI方式的前端界面，需增加以下端点：

- GET `/api/sdui/system/organization` - 组织管理页面UI配置
- GET `/api/sdui/system/role` - 角色管理页面UI配置
- GET `/api/sdui/system/user` - 用户管理页面UI配置
- GET `/api/sdui/system` - 系统管理主页UI配置

## 权限规则

1. **组织节点权限**:
   - 超级管理员可以访问所有节点
   - 普通用户只能访问分配给其角色的节点
   - 支持三级权限：view(查看)、manage(管理)、full(完全控制)
   - 创建子节点需要对父节点有manage权限
   - 删除节点需要对父节点有full权限

2. **角色权限**:
   - 只有超级管理员可以管理角色和权限
   - 系统预定义角色不能修改或删除
   - 每个用户可以拥有多个角色

## 实施计划

1. **第一阶段**: 基础数据模型和API开发 ✓
2. **第二阶段**: SDUI配置端点开发
3. **第三阶段**: 前端SDUI渲染引擎集成
4. **第四阶段**: 单元测试和文档完善

## 下一步工作

1. 开发SDUI页面配置生成器
2. 实现角色和用户管理页面的SDUI配置
3. 集成权限检查机制到SDUI渲染过程
4. 编写测试用例和操作文档 