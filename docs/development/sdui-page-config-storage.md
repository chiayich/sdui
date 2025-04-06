# SDUI页面配置存储方案

**日期**: 2024-06-06
**类别**: 架构/后端
**状态**: 已实施

## 设计目标

将SDUI页面配置从硬编码实现改为数据库存储方式，实现以下目标：

1. 支持页面配置的版本管理
2. 允许在运行时修改页面配置
3. 提供配置历史记录和回滚能力
4. 支持不同环境（测试、生产）使用不同配置版本

## 实现架构

### 数据模型设计

创建了`SDUIConfig`模型来存储SDUI页面配置：

```python
class SDUIConfig(Base):
    """SDUI页面配置模型"""
    __tablename__ = "sdui_configs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    config_data = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

字段说明：
- `code`: 配置唯一标识码（如system, system.organization）
- `name`: 配置名称
- `category`: 配置分类（如system, business）
- `version`: 配置版本号
- `config_data`: 完整UI配置JSON数据
- `is_active`: 是否启用

### CRUD操作

实现了完整的CRUD操作，包括：
1. 基本的创建、读取、更新、删除
2. 根据code获取最新版本配置
3. 根据分类获取配置列表
4. 创建新版本功能

关键方法：
```python
def get_latest_by_code(self, db: Session, *, code: str) -> Optional[SDUIConfig]:
    """获取某个配置的最新版本"""
    return db.query(self.model).filter(
        self.model.code == code,
        self.model.is_active == True
    ).order_by(desc(self.model.version)).first()

def create_new_version(self, db: Session, *, code: str, config_data: Dict[str, Any], user_id: str) -> SDUIConfig:
    """创建配置的新版本"""
    # 获取当前最新版本
    current = self.get_latest_by_code(db, code=code)
    if not current:
        raise ValueError(f"Config with code {code} not found")
    
    # 创建新版本
    new_version = SDUIConfig(
        code=current.code,
        name=current.name,
        category=current.category,
        version=current.version + 1,
        config_data=config_data,
        description=current.description,
        creator_id=user_id,
        updated_by=user_id
    )
    
    db.add(new_version)
    db.commit()
    db.refresh(new_version)
    return new_version
```

### API端点

创建了以下API端点：
1. `GET /api/sdui/{code}` - 获取指定配置的最新版本
2. `GET /api/sdui/configs/` - 获取配置列表（仅超级管理员）
3. `POST /api/sdui/configs/` - 创建新配置（仅超级管理员）
4. `PUT /api/sdui/configs/{code}` - 更新配置/创建新版本（仅超级管理员）

### 初始数据

为确保系统初始运行时有页面配置，实现了配置初始化逻辑：
```python
def create_initial_sdui_configs(db: Session) -> None:
    """创建初始SDUI配置"""
    configs_created = 0
    
    for config_data in DEFAULT_SDUI_CONFIGS:
        code = config_data["code"]
        existing = crud.sdui_config.get_by_code(db=db, code=code)
        
        if not existing:
            config_in = schemas.SDUIConfigCreate(
                code=code,
                name=config_data["name"],
                category=config_data["category"],
                config_data=config_data["config_data"],
                description=config_data.get("description", ""),
            )
            crud.sdui_config.create(db=db, obj_in=config_in)
            configs_created += 1
```

## 前端适配

更新了前端SDUI页面组件，使用新的API端点获取配置：
```vue
<template>
  <div class="sdui-page-container">
    <SDUIRenderer :schema="'/api/sdui/system'" />
  </div>
</template>
```

```vue
<template>
  <div class="sdui-page-container">
    <SDUIRenderer :schema="'/api/sdui/system.organization'" />
  </div>
</template>
```

```vue
<template>
  <div class="sdui-page-container">
    <SDUIRenderer :schema="'/api/sdui/system.role'" />
  </div>
</template>
```

## 配置管理流程

1. **开发环境**：
   - 初始配置通过代码定义在`DEFAULT_SDUI_CONFIGS`中
   - 数据库初始化时自动创建
   
2. **生产环境**：
   - 可通过API更新配置
   - 每次更新创建新的版本记录
   - 版本号自动递增
   
3. **配置迁移**：
   - 可导出配置为JSON文件
   - 在不同环境导入配置

## 优势与注意事项

**优势**：
1. 支持在线修改UI配置，无需发布新版本
2. 版本管理确保配置更改可追踪和回滚
3. 可以为不同环境维护不同配置版本
4. 支持配置的导入导出和备份

**注意事项**：
1. 配置修改需谨慎，确保JSON结构正确
2. 需考虑缓存机制，避免频繁数据库查询
3. 前端组件必须与后端配置格式兼容
4. 在生产环境更新配置前应在测试环境验证 