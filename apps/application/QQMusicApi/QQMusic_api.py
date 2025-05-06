from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import asyncio
import base64
import io
from enum import Enum

from qqmusic_api import search, sync
from qqmusic_api.login import (
    QR,
    LoginError,
    QRCodeLoginEvents,
    QRLoginType,
    check_qrcode,
    get_qrcode,
)

# 创建应用
qqmusic_app = FastAPI(title="QQ音乐API", description="QQ音乐API接口，提供搜索、登录等功能")

# 数据模型
class QRCodeResponse(BaseModel):
    code: int
    message: str
    qr_id: str
    qr_image: str

class LoginStatusResponse(BaseModel):
    code: int
    message: str
    status: str
    musicid: Optional[str] = None
    credential: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None

# 存储二维码和登录状态的字典
qrcode_cache = {}

# 二维码登录
@qqmusic_app.get("/login/qrcode/{login_type}", response_model=QRCodeResponse, operation_id="get_qrcode")
async def api_get_qrcode(login_type: str):
    """
    获取QQ音乐二维码登录的二维码
    
    Args:
        login_type: 登录类型，可选 qq 或 wx
    
    Returns:
        二维码信息
    """
    try:
        # 设置登录类型
        if login_type.lower() == "qq":
            login_type_enum = QRLoginType.QQ
        elif login_type.lower() == "wx":
            login_type_enum = QRLoginType.WX
        else:
            raise HTTPException(status_code=400, detail="登录类型错误，只支持 qq 或 wx")
        
        # 获取二维码
        qr = await get_qrcode(login_type_enum)
        qr_id = base64.b64encode(qr.id.encode()).decode()
        
        # 缓存二维码信息
        qrcode_cache[qr_id] = qr
        
        # 返回二维码信息和图片的base64编码
        qr_image = base64.b64encode(qr.data).decode()
        
        return {
            "code": 200,
            "message": "获取二维码成功",
            "qr_id": qr_id,
            "qr_image": qr_image
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取二维码失败: {str(e)}")

@qqmusic_app.get("/login/check/{qr_id}", response_model=LoginStatusResponse, operation_id="check_qrcode")
async def api_check_qrcode(qr_id: str):
    """
    检查二维码的扫描状态
    
    Args:
        qr_id: 二维码ID
    
    Returns:
        登录状态信息
    """
    try:
        # 从缓存获取二维码
        qr = qrcode_cache.get(qr_id)
        if not qr:
            raise HTTPException(status_code=404, detail="二维码不存在或已过期")
        
        # 检查扫码状态
        event, credential = await check_qrcode(qr)
        
        if event == QRCodeLoginEvents.DONE:
            # 登录成功，清除缓存
            del qrcode_cache[qr_id]
            return {
                "code": 200,
                "message": "登录成功",
                "status": "DONE",
                "musicid": credential.musicid,
                "credential": credential.model_dump() if hasattr(credential, "model_dump") else vars(credential)
            }
        elif event == QRCodeLoginEvents.TIMEOUT:
            # 二维码过期，清除缓存
            del qrcode_cache[qr_id]
            return {
                "code": 408,
                "message": "二维码已过期",
                "status": "TIMEOUT"
            }
        elif event == QRCodeLoginEvents.SCAN:
            return {
                "code": 201,
                "message": "二维码已扫描，等待确认",
                "status": "SCAN"
            }
        else:
            return {
                "code": 100,
                "message": "等待扫描",
                "status": "WAITING"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查二维码状态失败: {str(e)}")

# 搜索相关接口
@qqmusic_app.get("/search/general", response_model=SearchResponse, operation_id="general_search")
async def api_general_search(
    keyword: str, 
    page: int = Query(1, ge=1), 
    highlight: bool = Query(False)
):
    """
    综合搜索
    
    Args:
        keyword: 搜索关键词
        page: 页码，从1开始
        highlight: 是否高亮结果
    
    Returns:
        搜索结果
    """
    try:
        result = await search.general_search(keyword, page=page, highlight=highlight)
        return {
            "code": 200,
            "message": "搜索成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

class SearchTypeEnum(str, Enum):
    SONG = "song"
    ALBUM = "album"
    SINGER = "singer"
    PLAYLIST = "playlist"
    MV = "mv"
    LYRIC = "lyric"
    USER = "user"

@qqmusic_app.get("/search/by_type", response_model=SearchResponse, operation_id="search_by_type")
async def api_search_by_type(
    keyword: str,
    search_type: SearchTypeEnum,
    page: int = Query(1, ge=1),
    num: int = Query(20, ge=1, le=100),
    highlight: bool = Query(False)
):
    """
    按类型搜索
    
    Args:
        keyword: 搜索关键词
        search_type: 搜索类型
        page: 页码，从1开始
        num: 每页数量
        highlight: 是否高亮结果
    
    Returns:
        搜索结果
    """
    try:
        # 转换搜索类型
        search_type_map = {
            "song": search.SearchType.SONG,
            "album": search.SearchType.ALBUM,
            "singer": search.SearchType.SINGER,
            "playlist": search.SearchType.PLAYLIST,
            "mv": search.SearchType.MV,
            "lyric": search.SearchType.LYRIC,
            "user": search.SearchType.USER,
        }
        
        result = await search.search_by_type(
            keyword, 
            search_type=search_type_map.get(search_type),
            page=page,
            num=num,
            highlight=highlight
        )
        
        return {
            "code": 200,
            "message": "搜索成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@qqmusic_app.get("/search/quick", response_model=SearchResponse, operation_id="quick_search")
async def api_quick_search(keyword: str):
    """
    快速搜索
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        搜索结果
    """
    try:
        result = await search.quick_search(keyword)
        return {
            "code": 200,
            "message": "搜索成功",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

# 健康检查
@qqmusic_app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(qqmusic_app, host="0.0.0.0", port=8001)
