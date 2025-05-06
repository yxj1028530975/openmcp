from fastapi_mcp import FastApiMCP
import uvicorn
from fastapi import FastAPI, APIRouter, Request, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from common.server import server_app
import logging
import traceback
from application.DailyHotApi.dailyhot_api import *  # 导入 dailyhot_api 中的所有路由
from application.weather.weather_api import *  # 导入 weather_api 中的所有路由
# from common.api_list import *  # 导入 api_list 模块以注册API注册表路由

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MCP服务挂载
mcp = FastApiMCP(
    fastapi=server_app,
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
    
    uvicorn.run(server_app, host="0.0.0.0", port=8000)
