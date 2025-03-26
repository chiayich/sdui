# Python依赖安装优化

**日期**: 2023-11-28
**类别**: 开发环境/工具
**紧急程度**: 中

## 问题描述

在开发容器重建过程中，发现每次都会重新安装Python依赖包，即使`requirements.txt`文件没有更新。这导致了不必要的时间浪费，延长了开发环境准备时间。

## 问题分析

分析发现，在`/usr/local/bin/init.sh`脚本中，依赖安装逻辑过于简单，没有考虑增量安装和缓存机制：

```bash
# 后端依赖安装
if [ -f /workspace/backend/requirements.txt ]; then
    echo "👉 安装后端Python依赖..."
    cd /workspace/backend
    pip install -r requirements.txt
fi
```

这导致每次容器重建或启动时都会无条件执行`pip install -r requirements.txt`，不管依赖是否已经安装或者是否有变化。

## 解决思路

为了避免不必要的依赖重新安装，实现了基于文件哈希值的缓存机制：

1. 计算`requirements.txt`文件的MD5哈希值
2. 将哈希值保存在缓存文件中
3. 在下次启动时，比较当前哈希值与缓存的哈希值
4. 只有当哈希值不同（即`requirements.txt`有变化）时，才重新安装依赖

同样的优化也应用于前端Node.js依赖的安装过程。

## 执行步骤

修改`/usr/local/bin/init.sh`脚本，添加依赖缓存检查机制：

```bash
# 后端依赖安装 - 优化以避免不必要的重新安装
if [ -f /workspace/backend/requirements.txt ]; then
    echo "👉 检查后端Python依赖..."
    cd /workspace/backend
    
    # 创建缓存目录
    mkdir -p /workspace/.cache
    
    # 计算requirements.txt的哈希值
    REQUIREMENTS_HASH=$(md5sum requirements.txt | cut -d ' ' -f 1)
    HASH_FILE="/workspace/.cache/requirements_hash"
    
    # 检查是否需要重新安装
    REINSTALL=0
    if [ ! -f "$HASH_FILE" ]; then
        echo "📦 首次安装Python依赖..."
        REINSTALL=1
    else
        PREVIOUS_HASH=$(cat "$HASH_FILE")
        if [ "$REQUIREMENTS_HASH" != "$PREVIOUS_HASH" ]; then
            echo "📦 检测到requirements.txt有变更，重新安装依赖..."
            REINSTALL=1
        else
            echo "✅ Python依赖未变更，跳过安装"
        fi
    fi
    
    if [ "$REINSTALL" -eq 1 ]; then
        echo "📦 安装Python依赖中..."
        pip install -r requirements.txt
        echo "$REQUIREMENTS_HASH" > "$HASH_FILE"
        echo "✅ Python依赖安装完成"
    fi
fi
```

## 结果验证

修改后的脚本在容器重建时表现如下：

1. 首次运行：计算哈希值并安装依赖
2. 后续运行（无依赖变化）：检测到哈希值未变，跳过安装
3. 依赖变化后：检测到哈希值变化，执行增量安装

这显著减少了开发环境准备时间，特别是在频繁重建容器的场景下。

## 相关资源

- [Shell脚本最佳实践](https://google.github.io/styleguide/shellguide.html)
- [MD5哈希在文件变更检测中的应用](https://en.wikipedia.org/wiki/MD5)

## 注意事项

1. 哈希缓存文件存储在`/workspace/.cache`目录下，确保此目录在容器重建过程中不会被删除。

2. 如需强制重新安装所有依赖，可以手动删除缓存文件：
   ```bash
   rm -f /workspace/.cache/requirements_hash /workspace/.cache/node_hash
   ```

3. 此优化不会影响`pip`对单个依赖包的版本管理，只是避免了整体重新安装的过程。 