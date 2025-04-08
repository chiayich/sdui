# SQLAlchemy模型初始化问题修复

**日期**: 2024-03-22
**类别**: 后端
**紧急程度**: 高

## 问题描述

在初始化SQLAlchemy模型时遇到两个主要问题：
1. 无法导入 `app.db.base_class`
2. SQLAlchemy映射器初始化失败，找不到`users`表来建立外键关系

## 问题分析

1. 缺少必要的基础类文件和包结构
2. 数据库配置不完整
3. 模型之间的依赖关系未正确处理

## 解决思路

1. 创建完整的包结构和必要的基础文件
2. 实现数据库配置管理
3. 确保所有模型在初始化时被正确加载

## 执行步骤

1. 创建基础类文件：
   - 创建 `backend/app/db/base_class.py`
   - 创建 `backend/app/db/__init__.py`
   - 创建 `backend/app/db/base.py`

2. 创建数据库配置：
   - 创建 `backend/app/db/session.py`
   - 创建 `backend/app/core/config.py`
   - 创建 `backend/app/core/__init__.py`

3. 更新模型定义，确保正确使用schema

## 结果验证

需要运行以下步骤来验证修复：
1. 确保所有依赖已安装
2. 检查数据库连接配置
3. 运行应用，验证模型是否正确初始化

## 相关资源

- [SQLAlchemy文档 - Declarative Models](https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html)
- [FastAPI with SQLAlchemy](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## 注意事项

1. 确保数据库配置信息正确
2. 注意模型之间的依赖顺序
3. 所有表都应该在`sdui_schema`模式下创建 