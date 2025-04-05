# FastAPI 中间件请求阻塞问题

**日期**: 2023-03-29
**类别**: 后端
**紧急程度**: 高

## 问题描述

在 SDUI 后端应用中，我们遇到了 FastAPI 应用无响应的问题。具体表现为：当客户端发送请求时，请求会被接收但不会得到响应，应用服务器看起来像是被阻塞。通过调试发现，请求卡在了自定义的 `LoggingMiddleware` 中的 `call_next` 函数调用处，导致请求处理链中断。

## 问题分析

通过代码审查和日志分析，我们发现问题出在以下几个方面：

1. **请求体读取问题**：在中间件中，我们尝试通过 `await request.body()` 读取请求体，然后通过 `request._body = request_body_bytes` 重置请求体供后续处理。这种方式在某些情况下会导致请求流被错误地消费，特别是在处理大型请求体或流式传输数据时。

2. **中间件顺序问题**：中间件的注册顺序会影响请求处理流程。在原来的实现中，`LoggingMiddleware` 被注册在 CORS 中间件之前，这可能导致一些预检请求（preflight requests）没有被正确处理。

3. **请求流消费后没有正确重置**：虽然我们使用 `request._body` 尝试重置请求体，但这不是官方支持的方法，可能导致流状态不一致。

4. **错误处理不完善**：当读取请求体出错时，我们记录了错误但没有确保请求能够继续处理。

## 解决思路

针对以上问题，我们采取了以下解决思路：

1. **避免预先读取请求体**：最简单和安全的解决方案是完全避免在中间件中读取请求体。我们可以只记录请求的基本信息（如方法、URL、查询参数等），而不尝试访问请求体。

2. **调整中间件顺序**：将 `LoggingMiddleware` 放在中间件链的最后注册，这样它实际上会成为处理链中的第一个中间件（因为中间件的执行顺序与注册顺序相反）。

3. **简化日志记录**：减少在关键请求路径上的复杂操作，优化性能并减少出错可能。

## 执行步骤

1. **修改 `main.py` 中的中间件注册顺序**：

```python
# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，方便调试
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# 应用日志中间件（放在最后添加，这样它会第一个执行）
app.add_middleware(LoggingMiddleware)
```

2. **优化 `logging_middleware.py` 中的请求处理逻辑**：

```python
async def dispatch(self, request: Request, call_next):
    # 生成请求ID
    request_id = str(uuid.uuid4())

    # 记录请求开始时间
    start_time = time.time()
    
    # 记录基本请求信息，不尝试读取请求体
    logger_service.log(
        level="INFO",
        message=f"开始处理请求: {request.method} {request.url}",
        source="api",
        metadata={"request_id": request_id}
    )

    try:
        # 调用下一个中间件或路由处理器
        response = await call_next(request)
        
        # 计算请求处理时间
        duration = (time.time() - start_time) * 1000  # 毫秒

        # 记录日志
        logger_service.log_api_request(
            request_id=request_id,
            method=request.method,
            path=str(request.url),
            status_code=response.status_code,
            duration_ms=duration,
            request_data=None  # 不记录请求体，避免性能问题
        )

        return response
    except Exception as e:
        # 记录异常
        # ... 异常处理逻辑 ...
        raise
```

## 结果验证

修改后，我们进行了以下验证：

1. 使用 `curl` 和浏览器发送不同类型的请求（GET、POST等），所有请求都能正常响应
2. 压力测试显示，修改后的中间件不再会导致请求阻塞
3. 所有正常的日志记录功能仍然正常工作
4. 应用启动时不再有相关警告信息

## 相关资源

- [FastAPI 中间件文档](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Starlette 中间件源码](https://github.com/encode/starlette/blob/master/starlette/middleware/base.py)
- [相关问题在 GitHub 上的讨论](https://github.com/tiangolo/fastapi/issues/394)

## 注意事项

1. **请求体处理**：在中间件中处理请求体时需要格外小心。一般原则是，除非绝对必要，否则不要在中间件中尝试读取请求体。

2. **中间件顺序**：中间件的执行顺序与注册顺序相反，这一点在设计多个中间件的协作时需要特别注意。

3. **性能考虑**：日志中间件应尽量轻量化，避免在请求处理主路径上执行耗时操作。

4. **异步上下文**：在异步框架中，确保所有可能的阻塞操作都使用正确的异步方法，避免意外地阻塞事件循环。

5. **监控与告警**：应考虑添加请求处理时间监控，以便及早发现类似的性能问题。 