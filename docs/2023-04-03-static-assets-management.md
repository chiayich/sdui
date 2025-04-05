# 静态资源管理与目录规范实施

**日期**: 2023-04-03
**类别**: 前端
**紧急程度**: 中

## 问题描述

项目需要合理管理静态资源（如图片、Logo等），目前缺少统一的目录结构和命名规范，导致资源引用路径混乱，且没有考虑后续可能需要的OSS存储迁移方案。

## 问题分析

静态资源管理存在以下问题：

1. 缺少统一的目录结构，导致资源分散在不同位置
2. 直接使用绝对路径硬编码引用资源，不利于后续迁移
3. 没有资源分类和命名规范，可能导致冲突和混乱
4. 未考虑后续可能的CDN和OSS集成需求

## 解决思路

1. 建立清晰的静态资源目录结构，按资源类型分类
2. 制定资源命名规范，便于管理和查找
3. 使用统一的引用方式，便于后续迁移
4. 预留OSS迁移的实施方案

## 执行步骤

1. 创建统一的静态资源目录结构：

```bash
mkdir -p frontend/public/static/{images,logos,icons}
```

2. 制定资源命名规范，如：

- 图片：`[模块]-[用途]-[尺寸/版本].[扩展名]`
- Logo：`[品牌]-logo-[尺寸/版本].[扩展名]`
- 图标：`[功能]-[状态].[扩展名]`

3. 更新资源引用路径：

```javascript
// 更新前
logo: '/logo.png',

// 更新后
logo: '/static/logos/brand-logo.png',
```

4. 创建详细的资源管理文档

```bash
# 创建资源管理文档
touch docs/assets-management.md
```

5. 添加样例资源：

```bash
curl -o frontend/public/static/logos/brand-logo.png \
  "https://placehold.co/120x40/002140/ffffff/png?text=元气森林"
```

## 结果验证

1. 目录结构创建成功：
   - `frontend/public/static/images/`
   - `frontend/public/static/logos/`
   - `frontend/public/static/icons/`

2. 资源引用路径已更新，指向新的目录结构

3. 资源管理文档已创建，包含详细的规范和指南

4. 示例Logo已成功添加到正确目录

## 相关资源

- [资源管理文档](/docs/assets-management.md)
- [Vue公共目录规范](https://cli.vuejs.org/guide/html-and-static-assets.html#the-public-folder)

## 注意事项

1. 在部署过程中需要确保静态资源正确复制到构建输出目录
2. 后续考虑实现静态资源的自动化上传到OSS服务
3. 当前实现支持本地开发和测试环境，生产环境可能需要根据具体部署方式调整 