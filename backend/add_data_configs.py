from app.db.session import SessionLocal
from app.schemas.sdui_config import SDUIConfigCreate
from app.crud.crud_sdui_config import sdui_config

def add_data_configs():
    db = SessionLocal()
    try:
        # 添加门店数据配置
        stores_data = [
            {"value": "store1", "label": "宝胜金华通道中心仓"},
            {"value": "store2", "label": "宝胜金华通道北仓"},
            {"value": "store3", "label": "宝胜杭州西湖店"},
            {"value": "store4", "label": "宝胜上海静安店"}
        ]
        
        stores_config = sdui_config.get_by_code(db, code="data/stores")
        if not stores_config:
            sdui_config_in = SDUIConfigCreate(
                code="data/stores",
                name="门店列表数据",
                config_type="data",
                content={"content": stores_data}
            )
            stores_config = sdui_config.create(db, obj_in=sdui_config_in)
            print("门店列表数据配置创建成功")
        else:
            print("门店列表数据配置已存在")
        
        # 添加最近订单数据配置
        orders_data = [
            {
                "orderNo": "DD2024030100001",
                "status": "待处理",
                "store": "宝胜金华通道中心仓",
                "createTime": "2024-03-01 10:23:45",
                "amount": 4150.00
            },
            {
                "orderNo": "DD2024030100002",
                "status": "处理中",
                "store": "宝胜金华通道北仓",
                "createTime": "2024-03-01 09:15:22",
                "amount": 3280.50
            },
            {
                "orderNo": "DD2024030100003",
                "status": "已完成",
                "store": "宝胜杭州西湖店",
                "createTime": "2024-02-29 15:45:10",
                "amount": 6430.00
            },
            {
                "orderNo": "DD2024030100004",
                "status": "已完成",
                "store": "宝胜上海静安店",
                "createTime": "2024-02-28 14:22:33",
                "amount": 5120.75
            }
        ]
        
        orders_config = sdui_config.get_by_code(db, code="data/recent-orders")
        if not orders_config:
            sdui_config_in = SDUIConfigCreate(
                code="data/recent-orders",
                name="最近订单数据",
                config_type="data",
                content={"content": orders_data}
            )
            orders_config = sdui_config.create(db, obj_in=sdui_config_in)
            print("最近订单数据配置创建成功")
        else:
            print("最近订单数据配置已存在")
            
    finally:
        db.close()

if __name__ == "__main__":
    add_data_configs() 