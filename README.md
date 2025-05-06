# OpenMCP平台

基于FastAPI的开放式MCP（Multi-Channel Protocol）平台，提供统一接口配置和热榜数据聚合服务。

## 概述

OpenMCP平台旨在通过简单的MCP配置，集成多种数据源和服务，实现统一接口调用。目前已支持50多个热门平台的热榜数据，未来将持续扩展更多功能。

## MCP配置

MCP配置文件位于 `~/.cursor/mcp.json`，基本结构如下：

```json
{
  "mcpServers": {
    "openmcp-sse": {
      "url": "http://127.0.0.1:8000/mcp",
      "name": "openmcp-sse"
    }
  }
}
```

您可以在此配置多个MCP服务器，系统将自动加载并提供统一的访问入口。

## 项目结构

OpenMCP项目包含两个主要部分：

1. **后端服务(apps目录)**：基于FastAPI的MCP服务实现，提供各类数据接口
2. **前端界面(ui目录)**：基于Vue.js的用户界面，用于MCP配置展示和数据可视化

### 后端服务

已集成的服务模块包括：

#### 1. 热榜数据服务 (dailyhot-sse)

提供知乎、微博、B站等50多个平台的热榜数据。

- 获取指定平台热榜：`/hot/{platform}`
- 知乎热榜：`/zhihu`
- 微博热搜：`/weibo`
- B站热榜：`/bilibili`
- 新闻热榜(聚合)：`/news`

##### 支持的平台分类

| 分类 | 包含平台 |
|------|----------|
| 社交媒体 | 知乎、微博、豆瓣、虎扑、NGA等 |
| 视频平台 | B站、抖音、快手、AcFun等 |
| 新闻资讯 | 澎湃、腾讯新闻、新浪新闻等 |
| 科技数码 | IT之家、36氪、爱范儿等 |
| 技术开发 | CSDN、掘金、V2EX、GitHub等 |
| 游戏动漫 | 英雄联盟、原神、米游社等 |
| 生活服务 | 天气预警、地震速报、历史上的今天 |

详细支持的平台列表请参考 [热榜服务文档](apps/application/DailyHotApi/README.md)。

#### 2. 天气服务 (weather-sse)

通过城市名称（中国城市使用拼音）或经纬度获取天气信息。

- 基于城市名称获取天气：`/get_weather_cityname`
- 基于经纬度获取天气：`/get_weather_latitude_longitude`

### 前端界面

前端项目提供直观的用户界面，方便查看MCP配置和使用各项服务。

#### 主要功能

- **首页**：项目概览、服务状态和最新动态
- **MCP配置文档**：详细的配置说明和示例
- **服务分类浏览**：按分类查看所有可用服务
- **热榜数据展示**：可视化展示各平台热榜数据

#### 技术栈

- **Vue.js 3**：前端框架
- **Tailwind CSS**：样式框架
- **Vite**：构建工具
- **Vue Router**：路由管理

## 系统架构

OpenMCP平台采用模块化架构设计：

1. **核心层**：基于FastAPI的Web服务框架
2. **MCP层**：Multi-Channel Protocol实现，提供统一调用接口
3. **应用层**：各个独立的服务模块（热榜数据、天气等）
4. **数据层**：依赖的外部数据源和服务
5. **表现层**：Vue.js前端界面，展示配置和数据

![架构图](docs/architecture.png)

## 功能特点

- **统一接口**：通过MCP协议统一调用各种数据服务
- **简单配置**：简洁的JSON配置文件，易于设置和管理
- **数据聚合**：集成多个热门平台的实时数据
- **高性能**：基于异步FastAPI框架，提供高并发支持
- **可扩展性**：易于添加新的数据源和服务
- **完整文档**：提供详细的API文档和配置说明
- **友好界面**：直观的用户界面，便于使用和管理

## 部署说明

### 后端部署

1. 安装依赖:

```bash
pip install -r requirements.txt
```

2. (可选) 启动DailyHotApi容器:

```bash
cd apps/application/DailyHotApi
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

服务默认在 http://localhost:8000 上运行。

5. 配置MCP客户端:

在 `~/.cursor/mcp.json` 文件中添加服务配置，示例如下:

```json
{
  "mcpServers": {
    "openmcp-sse": {
      "url": "http://127.0.0.1:8000/mcp",
      "name": "openmcp-sse"
    }
  }
}
```

### 前端部署

1. 安装依赖:

```bash
cd ui
npm install
```

2. 开发模式运行:

```bash
npm run dev
```

3. 构建生产版本:

```bash
npm run build
```

4. 预览生产构建:

```bash
npm run preview
```

前端默认在 http://localhost:5173 上运行，可通过环境变量或配置文件修改后端API地址。

## API文档与调用

启动服务后，可通过以下方式查看和调用API：

- Swagger UI文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc
- MCP配置文档：http://localhost:8000/api-registry
- 前端界面：http://localhost:5173

### MCP调用示例

#### 通过MCP接口调用

```javascript
// 获取知乎热榜
async function getZhihuHot() {
  const response = await fetch('http://127.0.0.1:8000/mcp', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      "operation": "openmcp-sse.get_zhihu_hot",
      "parameters": {}
    })
  });
  return await response.json();
}
```

#### 直接API调用

```javascript
// 获取知乎热榜
async function getZhihuHot() {
  const response = await fetch('http://127.0.0.1:8000/zhihu');
  return await response.json();
}

// 获取微博热搜
async function getWeiboHot() {
  const response = await fetch('http://127.0.0.1:8000/weibo');
  return await response.json();
}
```

## 响应数据格式

所有API返回统一的JSON格式：

```json
{
  "code": 200,
  "message": "Success",
  "title": "热榜标题",
  "subtitle": "热榜副标题",
  "data": [
    {
      "title": "热点标题",
      "url": "链接地址",
      "hot": "热度值",
      "img": "图片URL（可选）",
      "mobileUrl": "移动端链接（可选）",
      "desc": "描述（可选）"
    }
    // 更多数据项...
  ]
}
```

## 开发指南

### 后端开发

要为OpenMCP平台添加新的服务模块，请遵循以下步骤：

1. 在`apps/application`目录中创建新的服务子目录
2. 实现服务的FastAPI应用
3. 在`common/api_list.py`中注册API并添加适当的标签
4. 编写详细的README文档

### 前端开发

要为前端添加新功能或页面：

1. 在`ui/src/views`目录添加新的视图组件
2. 在`ui/src/router`中注册新路由
3. 实现相应的组件和逻辑
4. 更新导航菜单

详细开发指南请参考[开发文档](docs/development.md)。

## 常见问题

### 如何添加自定义MCP服务器？

在配置文件中的mcpServers对象中添加新的服务器配置，指定url和name属性即可。配置文件位于~/.cursor/mcp.json。

### 如何排查MCP连接问题？

请检查配置文件格式是否正确，服务器URL是否可访问，以及网络连接状态。您可以使用curl或浏览器直接访问MCP服务URL来测试连接。

### 数据更新频率是多少？

不同平台的数据更新频率不同，大多数热榜数据每5-15分钟更新一次，确保数据的及时性。

### 如何自定义前端接口地址？

在前端项目根目录创建`.env.local`文件，设置`VITE_API_BASE_URL`环境变量：

```
VITE_API_BASE_URL=http://your-api-server:8000
```

## 技术栈

**后端:**
- **FastAPI**: 高性能Web框架
- **FastApiMCP**: 多通道协议实现
- **Docker**: 容器化部署
- **httpx**: 异步HTTP客户端
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据校验和序列化

**前端:**
- **Vue.js 3**: 前端框架
- **Tailwind CSS**: 样式框架
- **Vue Router**: 路由管理
- **Vite**: 构建工具

## 贡献

欢迎提交Issue和Pull Request，共同改进此项目！

## 许可

本项目采用MIT许可证。详情请参阅LICENSE文件。