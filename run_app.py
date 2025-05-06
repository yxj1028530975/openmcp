#!/usr/bin/env python3
"""
OpenMCP 应用程序启动入口
用于在Docker容器中启动应用程序
"""

import uvicorn
import os
import sys

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

# 直接导入FastAPI应用实例
from apps.common.server import server_app

if __name__ == "__main__":
    # 获取环境变量或使用默认值
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    
    # 打印Python路径信息，便于调试
    print(f"Python Path: {sys.path}")
    print(f"Current Directory: {os.getcwd()}")
    
    # 启动应用
    uvicorn.run(
        server_app, 
        host=host, 
        port=port,
        log_level="info",
        reload=False
    ) 