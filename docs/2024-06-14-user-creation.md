# 超级管理员账号创建问题与解决方案

## 问题描述

在使用登录API时遇到以下错误:

```json
[ 
  { 
    "type": "missing", 
    "loc": [ "body", "username" ], 
    "msg": "Field required", 
    "input": null, 
    "url": "https://errors.pydantic.dev/2.4/v/missing" 
  }, 
  { 
    "type": "missing", 
    "loc": [ "body", "password" ], 
    "msg": "Field required", 
    "input": null, 
    "url": "https://errors.pydantic.dev/2.4/v/missing" 
  } 
]
```

这表明在向登录API发送请求时，没有提供必需的 `username` 和 `password` 字段。

## 解决方案

1. 确保已正确创建超级管理员账号（默认: admin/admin）
   - 已在 `backend/app/core/config.py` 中将默认超级管理员密码从 `admin123` 修改为 `admin`
   - 调用 `init_db.py` 初始化数据库，创建超级管理员

2. 登录时的正确请求格式:
   - 登录API端点: `/api/v1/login/access-token`
   - 请求方式: POST
   - 内容类型: `application/x-www-form-urlencoded` 或 通过 FormData 发送
   - 必需参数:
     - username: admin
     - password: admin

3. 前端登录代码需确保:
   - 使用正确的API地址
   - 正确设置请求头和数据格式
   - 使用FormData或适当的格式发送用户名和密码

## 当前配置信息

- 超级管理员账号: admin
- 超级管理员邮箱: admin@example.com
- 默认密码: admin
- 配置文件位置: `backend/app/core/config.py`

## 示例登录请求

```javascript
// FormData方式
const formData = new FormData();
formData.append('username', 'admin');
formData.append('password', 'admin');

const response = await axios.post('/api/v1/login/access-token', formData);
```

或

```javascript
// URLSearchParams方式
const params = new URLSearchParams();
params.append('username', 'admin');
params.append('password', 'admin');

const response = await axios.post('/api/v1/login/access-token', params);
``` 