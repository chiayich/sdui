// 模拟门店列表
export const mockStores = [
  { value: 'store1', label: '宝胜金华通道中心仓' },
  { value: 'store2', label: '宝胜金华通道北仓' },
  { value: 'store3', label: '宝胜杭州西湖店' },
  { value: 'store4', label: '宝胜上海静安店' }
];

// 模拟最近订单
export const mockRecentOrders = [
  {
    orderNo: 'DD2024030100001',
    status: '待处理',
    store: '宝胜金华通道中心仓',
    createTime: '2024-03-01 10:23:45',
    amount: 4150.00
  },
  {
    orderNo: 'DD2024030100002',
    status: '处理中',
    store: '宝胜金华通道北仓',
    createTime: '2024-03-01 09:15:22',
    amount: 3280.50
  },
  {
    orderNo: 'DD2024030100003',
    status: '已完成',
    store: '宝胜杭州西湖店',
    createTime: '2024-02-29 15:45:10',
    amount: 6430.00
  },
  {
    orderNo: 'DD2024030100004',
    status: '已完成',
    store: '宝胜上海静安店',
    createTime: '2024-02-28 14:22:33',
    amount: 5120.75
  }
]; 