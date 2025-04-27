from fastapi_mcp import FastApiMCP
import uvicorn
from fastapi import FastAPI, APIRouter, Request, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from weather.weather_api import weather_app
from DailyHotApi.dailyhot_api import dailyhot_app
import logging
import traceback

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建一个主FastAPI应用
main_app = FastAPI(title="OpenMCP API", description="OpenMCP API服务集合")

# 添加CORS中间件
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 模型定义
class ApiEndpoint(BaseModel):
    name: str
    path: str
    method: str
    description: str
    params: Optional[List[Dict[str, Any]]] = None

class ApiInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    endpoints: List[ApiEndpoint]

class ApiListResponse(BaseModel):
    apis: List[ApiInfo]

@main_app.get("/api-registry/apis", response_model=ApiListResponse)
async def get_apis():
    """
    获取所有可用API的列表
    """
    apis = [
        {
            "id": "weather",
            "name": "天气信息API",
            "description": "通过城市名称（中国城市使用拼音）或经纬度获取天气信息",
            "category": "天气服务",
            "endpoints": [
                {
                    "name": "城市名称查询天气",
                    "path": "/weather/get_weather/cityname",
                    "method": "POST",
                    "description": "通过城市名称（中国城市使用拼音）获取天气信息",
                    "params": [
                        {"name": "cityname", "type": "string", "description": "城市名称（中国城市使用拼音）"}
                    ]
                },
                {
                    "name": "经纬度查询天气",
                    "path": "/weather/get_weather/latitude_longitude",
                    "method": "POST",
                    "description": "通过经纬度获取天气信息",
                    "params": [
                        {"name": "latitude", "type": "number", "description": "纬度"},
                        {"name": "longitude", "type": "number", "description": "经度"}
                    ]
                }
            ]
        },
        {
            "id": "dailyhot",
            "name": "今日热榜API",
            "description": "提供知乎、微博、B站等50多个平台的热榜数据",
            "category": "热榜服务",
            "endpoints": [
                {"name": "知乎热榜", "path": "/dailyhot/zhihu", "method": "GET", "description": "获取知乎热榜数据"},
                {"name": "微博热搜", "path": "/dailyhot/weibo", "method": "GET", "description": "获取微博热搜榜数据"},
                {"name": "B站热榜", "path": "/dailyhot/bilibili", "method": "GET", "description": "获取B站热榜数据"},
                {"name": "新闻热榜", "path": "/dailyhot/news", "method": "GET", "description": "获取新闻热榜 (聚合百度、网易等新闻源)"},
                {"name": "AcFun排行榜", "path": "/dailyhot/acfun", "method": "GET", "description": "获取AcFun排行榜数据"},
                {"name": "知乎日报", "path": "/dailyhot/zhihu-daily", "method": "GET", "description": "获取知乎日报推荐榜"},
                {"name": "百度热搜", "path": "/dailyhot/baidu", "method": "GET", "description": "获取百度热搜榜数据"},
                {"name": "抖音热点", "path": "/dailyhot/douyin", "method": "GET", "description": "获取抖音热点榜数据"},
                {"name": "快手热点", "path": "/dailyhot/kuaishou", "method": "GET", "description": "获取快手热点榜数据"},
                # 更多热榜接口...这里只列出部分
            ]
        }
    ]
    return {"apis": apis}

# 使用FastAPI的mount方法挂载子应用
main_app.mount("/weather", weather_app)
main_app.mount("/dailyhot", dailyhot_app)

# MCP服务挂载
mcp = FastApiMCP(
    fastapi=main_app,
    name="openmcp",
    description="OpenMCP API服务集合，包含天气信息、热榜数据等多种API",
    describe_all_responses=True,
    describe_full_response_schema=True
)
mcp.mount()

if __name__ == "__main__":
    # 使用包含所有路由的主应用
    import nest_asyncio
    nest_asyncio.apply()
    
    uvicorn.run(main_app, host="0.0.0.0", port=8000)
