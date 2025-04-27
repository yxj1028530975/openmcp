# OpenMCP平台

基于FastAPI和FastApiMCP的开放式MCP（Multi-Channel Protocol）平台，集成多种服务功能。

## 已集成服务

### 1. 天气服务 (weather-sse)

通过城市名称（中国城市使用拼音）或经纬度获取天气信息。

- 基于城市名称获取天气：`/get_weather/cityname`
- 基于经纬度获取天气：`/get_weather/latitude_longitude`

详细说明请查看 [天气服务文档](apps/weather/README.md)。

### 2. 今日热榜服务 (dailyhot-sse)

提供知乎、微博、B站等50多个平台的热榜数据。

- 获取所有可用热榜：`/routes`
- 获取指定平台热榜：`/hot/{platform}`
- 知乎热榜：`/zhihu`
- 微博热搜：`/weibo`
- B站热榜：`/bilibili`
- 新闻热榜(聚合)：`/news`
- 其他平台热榜：支持共42个热门平台

详细说明请查看 [今日热榜服务文档](apps/DailyHotApi/README.md)。

## 系统架构

OpenMCP平台采用模块化架构设计：

1. **核心层**：基于FastAPI的Web服务框架
2. **MCP层**：Multi-Channel Protocol实现，提供统一调用接口
3. **应用层**：各个独立的服务模块（天气、热榜等）
4. **数据层**：依赖的外部服务和数据源

![架构图](docs/architecture.png)

## 功能特点

- **多协议支持**：通过MCP统一多种API调用方式
- **模块化设计**：每个服务独立开发和部署
- **高性能**：基于异步FastAPI框架构建
- **易扩展**：简单添加新服务到MCP系统
- **容器化**：支持Docker容器部署
- **完整文档**：每个服务都有详细的API文档

## 部署说明

1. 安装依赖:

```bash
pip install -r requirements.txt
```

2. 启动DailyHotApi容器:

```bash
cd apps/DailyHotApi
docker-compose up -d
```

3. (可选) 设置环境变量:

```bash
# 如果DailyHotApi运行在其他地址，可以设置环境变量
export DAILYHOT_API_URL=http://your-host:6688
```

4. 启动MCP服务:

```bash
# 使用主启动脚本
python run_app.py

# 或者从apps目录启动
cd apps
PYTHONPATH=$PYTHONPATH:.. python main.py
```

默认情况下，服务将在 http://localhost:8000 上运行。

## API文档

启动服务后，可以访问以下地址查看API文档：

- OpenAPI文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc

### MCP调用

本平台支持通过MCP协议统一调用所有服务：

1. MCP入口点：`http://localhost:8000/mcp`
2. 请求方法：POST
3. 请求格式：请参考[FastApiMCP文档](https://github.com/microsoft/FastAPI-MCP)

示例调用（使用curl）：
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "operation": "dailyhot-sse.get_zhihu_hot",
    "parameters": {}
  }'
```

## 开发指南

要为OpenMCP平台添加新的服务模块，请遵循以下步骤：

1. 在`apps`目录中创建新的服务子目录
2. 实现服务的FastAPI应用
3. 编写详细的README文档
4. 注册服务到MCP系统

详细开发指南请参考[开发文档](docs/development.md)。

## 技术栈

- **FastAPI**: 高性能Web框架
- **FastApiMCP**: 多通道协议实现
- **Docker**: 容器化部署
- **httpx**: 异步HTTP客户端
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据校验和序列化

## 贡献

欢迎提交Issue和Pull Request，共同改进此项目！

## 许可

本项目采用MIT许可证。详情请参阅LICENSE文件。