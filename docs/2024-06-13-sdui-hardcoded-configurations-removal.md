# 移除硬编码SDUI配置，转为数据库驱动方式

**日期**: 2024-06-13
**类别**: 后端/架构
**紧急程度**: 中

## 问题描述

系统中的SDUI配置当前以Python代码形式硬编码在`sdui_service.py`文件中，通过`DEFAULT_SDUI_CONFIGS`常量定义。这导致以下问题：

1. 修改配置需要修改代码并重新部署应用
2. 缺少配置的版本控制和历史记录
3. 难以实现动态配置管理和在线编辑功能
4. 配置中存在JavaScript的布尔值（`true`/`false`）而不是Python布尔值（`True`/`False`）

## 问题分析

SDUI（服务端驱动UI）框架需要将UI配置从代码中分离出来，以支持：

1. 配置的动态加载和热更新
2. 通过后台管理页面进行配置修改
3. 配置的版本控制和回滚功能
4. 减少部署次数，提高系统灵活性

当前的实现方式将配置硬编码在服务代码中，违背了SDUI的设计理念，需要将配置数据迁移到数据库中，并修改相关服务逻辑以从数据库加载配置。

## 解决思路

1. 创建一个JSON配置文件作为配置数据的源
2. 修改迁移脚本，从JSON文件加载配置到数据库
3. 修改服务层代码，移除硬编码配置，改为从数据库获取配置
4. 优化`get_ui_config`等函数，提供完全基于数据库的配置获取逻辑
5. 确保特殊页面（如系统管理页面）能够根据用户权限动态生成配置

## 执行步骤

### 1. 修改配置迁移脚本

修改`backend/app/db/migrate_sdui_configs.py`以从JSON文件加载配置：

```python
import logging
import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from app import crud
from app.schemas.sdui_config import SDUIConfigCreate

logger = logging.getLogger(__name__)

# 配置文件路径
DEFAULT_CONFIGS_PATH = Path(__file__).parent.parent.parent / "sdui_configs.json"

def migrate_default_configs(db: Session) -> None:
    """将默认的SDUI配置从JSON文件迁移到数据库"""
    
    logger.info("开始迁移默认SDUI配置到数据库...")
    
    # 检查配置文件是否存在
    if not os.path.exists(DEFAULT_CONFIGS_PATH):
        logger.warning(f"配置文件不存在: {DEFAULT_CONFIGS_PATH}")
        return
    
    try:
        # 从JSON文件加载配置
        with open(DEFAULT_CONFIGS_PATH, 'r', encoding='utf-8') as f:
            configs = json.load(f)
        
        # 迁移每个配置
        for config in configs:
            # 检查配置是否已存在
            existing = crud.sdui_config.get_by_code(db, code=config["code"])
            
            if not existing:
                # 创建新配置
                sdui_config_in = SDUIConfigCreate(
                    code=config["code"],
                    name=config["name"],
                    config_type="page",  # 默认为页面类型
                    content=config["config_data"],
                    description=config.get("description", "")
                )
                
                try:
                    new_config = crud.sdui_config.create(db, obj_in=sdui_config_in)
                    logger.info(f"成功创建配置: {new_config.code}")
                except Exception as e:
                    logger.error(f"创建配置 {config['code']} 失败: {str(e)}")
            else:
                logger.info(f"配置 {config['code']} 已存在，跳过")
        
        logger.info("默认SDUI配置迁移完成")
    except Exception as e:
        logger.error(f"迁移过程发生错误: {str(e)}")
        raise
```

### 2. 创建配置数据文件

创建`backend/sdui_configs.json`文件，包含所有原有的配置数据，但修正布尔值为标准JSON格式：

```json
[
  {
    "code": "system",
    "name": "系统管理主页",
    "category": "system",
    "description": "系统管理主页UI配置",
    "config_data": {
      "type": "page",
      "id": "systemManagementPage",
      "title": "系统管理",
      "content": [
        // ... 具体配置内容
      ]
    }
  },
  // ... 其他配置
]
```

### 3. 修改服务层代码

修改`backend/app/services/sdui_service.py`，移除硬编码配置，优化服务函数：

```python
def get_ui_config(db: Session, code: str, user: User = None) -> Optional[Dict]:
    """
    根据配置代码从数据库获取UI配置
    如果是特殊页面（如system），则动态生成配置
    """
    # 特殊处理system页面，动态生成配置
    if code == "system" and user:
        return get_system_page_config(db, user)
    
    # 其他页面从数据库获取配置
    config = crud.sdui_config.get_by_code(db, code=code)
    if not config:
        return None
    
    return config.content
```

### 4. 解决数据库连接问题

执行迁移脚本时遇到了数据库连接问题，需要修改`backend/app/config.py`中的数据库配置：

```python
# 数据库设置
DB_HOST: str = os.getenv("DB_HOST", "localhost")  # 修改为localhost用于本地开发
DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
DB_USER: str = os.getenv("DB_USER", "huajin")  # 使用当前系统用户名
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")  # 本地开发环境通常不需要密码
DB_NAME: str = os.getenv("DB_NAME", "sdui")
DATABASE_URL: str = f"postgresql://{DB_USER}{':' + DB_PASSWORD if DB_PASSWORD else ''}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```

主要修改点：
1. 将数据库主机从`db`改为`localhost`，适应本地开发环境
2. 将数据库用户从`postgres`改为当前系统用户`huajin`
3. 移除默认密码，适应本地PostgreSQL配置
4. 优化连接字符串构建逻辑，处理空密码情况

## 结果验证

1. 运行迁移脚本，确认配置成功导入数据库：
```bash
python backend/migrate_configs.py
```

2. 启动应用，验证所有页面能够正确加载：
   - 系统管理页面能够根据用户权限动态生成
   - 组织架构、角色权限、用户管理等页面能从数据库加载配置

3. 通过后台管理页面修改配置，验证修改能够即时生效，无需重启应用

## 相关资源

- 修改的文件：
  - `backend/app/services/sdui_service.py`
  - `backend/app/db/migrate_sdui_configs.py`
  - `backend/sdui_configs.json`（新增）
  - `backend/app/config.py`（更新数据库配置）

- 相关数据库模型：
  - `app.models.sdui_config.SDUIConfig`

## 注意事项

1. 确保在部署前运行迁移脚本，将配置导入数据库
2. 监控首次加载性能，确保从数据库加载配置不会明显增加响应时间
3. 后续考虑实施缓存机制，减少重复数据库查询
4. 为确保向后兼容，保留对动态生成页面（如系统管理页面）的特殊处理
5. 需要调整应用配置以适应不同环境（开发、测试、生产），特别是数据库连接配置
6. 在容器化部署中，需要使用正确的数据库主机名（如Docker Compose中的服务名） 