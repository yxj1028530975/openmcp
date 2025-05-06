from common.server import server_app
from fastapi import APIRouter
from typing import List, Dict, Any
import inspect

# 创建路由器
api_registry_router = APIRouter(tags=["API注册表"], prefix="/api-registry")

@api_registry_router.get("/apis", summary="获取所有API路由信息", description="返回系统中所有注册的API路由信息，包括路径、方法、标签、参数和摘要等")
async def get_all_apis() -> Dict[str, Any]:
    """
    获取所有注册的API路由信息
    
    返回:
        Dict[str, Any]: 包含所有API路由信息的字典
    """
    api_routes = []
    
    # 遍历FastAPI应用中的所有路由
    for route in server_app.routes:
        # 检查路由是否有必要的属性
        if hasattr(route, "methods") and hasattr(route, "path"):
            # 提取tags信息，确保即使没有tags属性也能正常工作
            tags = []
            if hasattr(route, "tags") and route.tags:
                tags = list(route.tags)
            
            # 只有tags非空的路由才添加到结果中
            if tags:
                # 提取路由参数信息
                params = []
                if hasattr(route, "dependant") and hasattr(route.dependant, "path_params"):
                    for param in route.dependant.path_params:
                        param_info = {
                            "name": param.name,
                            "type": str(param.type_),
                            "required": param.required,
                            "location": "path"
                        }
                        params.append(param_info)
                
                # 提取查询参数
                if hasattr(route, "dependant") and hasattr(route.dependant, "query_params"):
                    for param in route.dependant.query_params:
                        param_info = {
                            "name": param.name,
                            "type": str(param.type_),
                            "required": param.required,
                            "location": "query"
                        }
                        params.append(param_info)
                
                # 提取路由处理函数的参数信息
                if hasattr(route, "endpoint") and callable(route.endpoint):
                    # 获取函数签名
                    try:
                        sig = inspect.signature(route.endpoint)
                        for param_name, param in sig.parameters.items():
                            # 排除已经添加的path和query参数，以及self/cls等特殊参数
                            if param_name not in ["self", "cls", "request"] and not any(p["name"] == param_name for p in params):
                                param_info = {
                                    "name": param_name,
                                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "unknown",
                                    "required": param.default == inspect.Parameter.empty,
                                    "location": "other"
                                }
                                params.append(param_info)
                    except (ValueError, TypeError):
                        # 处理无法获取签名的情况
                        pass
                
                route_info = {
                    "path": route.path,
                    "methods": list(route.methods),
                    "name": getattr(route, "name", ""),
                    "description": getattr(route, "description", ""),
                    "summary": getattr(route, "summary", ""),
                    "tags": tags,
                    "parameters": params
                }
                
                # 添加路由信息到列表
                api_routes.append(route_info)
    
    return {
        "total": len(api_routes),
        "apis": api_routes
    }

# 将路由器注册到主应用
server_app.include_router(api_registry_router)
