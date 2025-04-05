# 静态资源管理指南

## 目录结构

项目静态资源采用以下目录结构进行管理：

```
frontend/
  ├── public/            # 静态资源根目录（会被直接复制到构建输出目录）
  │   ├── static/        # 静态资源主目录
  │   │   ├── images/    # 通用图片资源
  │   │   ├── logos/     # 品牌Logo资源
  │   │   └── icons/     # 图标资源
  │   └── favicon.ico    # 网站图标
  └── src/
      └── assets/        # 需要通过构建工具处理的资源（如CSS）
```

## 资源分类与规范

### 图片资源（/static/images/）

- 通用页面图片
- 背景图片
- 产品图片

命名规范：`[模块]-[用途]-[尺寸/版本].[扩展名]`
例如：`product-thumbnail-sm.jpg`、`dashboard-background.png`

### Logo资源（/static/logos/）

- 品牌Logo
- 合作伙伴Logo

命名规范：`[品牌]-logo-[尺寸/版本].[扩展名]`
例如：`brand-logo.png`、`partner-logo-sm.png`

### 图标资源（/static/icons/）

- UI操作图标
- 功能图标

命名规范：`[功能]-[状态].[扩展名]`
例如：`edit-normal.svg`、`delete-hover.svg`

## 在代码中引用

### 在Vue模板中使用

```html
<!-- 绝对路径引用 -->
<img src="/static/images/banner.jpg" alt="Banner">

<!-- 相对路径引用（基于public目录） -->
<img :src="`${publicPath}/static/logos/brand-logo.png`" alt="Logo">
```

### 在CSS中使用

```css
.header-background {
  background-image: url('/static/images/header-bg.jpg');
}
```

## 资源优化建议

1. **图片格式选择**：
   - 照片类使用JPEG/JPG
   - 需要透明度的图像使用PNG
   - 矢量图使用SVG
   - 考虑使用WebP格式替代JPEG/PNG以获得更好的压缩率

2. **图片压缩**：
   - 上传前使用工具压缩图片（推荐：TinyPNG）
   - 确保图片尺寸适合使用场景，避免过大图片缩放显示

3. **图标管理**：
   - 优先使用SVG图标
   - 考虑使用图标字体（如Font Awesome）减少HTTP请求

## TODO：OSS迁移计划

后续会考虑将静态资源迁移至OSS服务，实现以下目标：

1. 降低源站服务器负载
2. 提高资源访问速度（CDN加速）
3. 实现资源版本管理

迁移步骤：

1. 选择合适的OSS服务商
   - [阿里云OSS](https://www.aliyun.com/product/oss)
   - [腾讯云COS](https://cloud.tencent.com/product/cos)
   - [七牛云对象存储](https://www.qiniu.com/products/kodo)
2. 编写资源上传脚本，集成到CI/CD流程
3. 更新引用方式，支持OSS路径前缀
4. 实现资源版本化命名，解决缓存问题

参考文档：
- [阿里云OSS前端直传实践](https://help.aliyun.com/document_detail/31927.html)
- [使用CDN加速OSS资源](https://help.aliyun.com/document_detail/123267.html) 