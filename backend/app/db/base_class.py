from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    SQLAlchemy 声明性基类
    """

    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:  # type: ignore
        return cls.__name__.lower()

    # 生成表参数
    @declared_attr
    def __table_args__(cls) -> dict:  # type: ignore
        return {"schema": "sdui_schema"}
