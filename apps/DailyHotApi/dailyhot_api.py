from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import httpx
import asyncio
import os
import json

# 可选导入chardet，用于自动检测编码
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False

dailyhot_app = FastAPI(title="今日热榜API", description="一个聚合热门数据的API接口，包含知乎、微博、B站等多个平台的热榜数据")

# 基本URL，优先使用环境变量配置
BASE_URL = os.environ.get("DAILYHOT_API_URL", "http://localhost:6688")

class RouteInfo(BaseModel):
    name: str
    path: str

class RoutesResponse(BaseModel):
    code: int
    count: int
    routes: List[RouteInfo]

class HotItem(BaseModel):
    title: str
    url: Optional[str] = None
    hot: Optional[Union[str, int]] = None
    img: Optional[str] = None
    mobileUrl: Optional[str] = None
    desc: Optional[str] = None

class HotListResponse(BaseModel):
    code: int
    message: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    data: Optional[List[HotItem]] = None

async def fetch_data(url: str) -> Dict[str, Any]:
    """从原始API获取数据"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"code": -1, "message": f"获取数据失败: {str(e)}"}

# @dailyhot_app.get("/routes", response_model=RoutesResponse, operation_id="get_routes")
# async def get_routes():
#     """
#     获取所有可用的热榜接口列表
    
#     Returns:
#         code: 状态码
#         count: 接口数量
#         routes: 接口列表
#     """
#     result = await fetch_data(f"{BASE_URL}/")
#     return result

@dailyhot_app.get("/hot/{platform}", response_model=HotListResponse, operation_id="get_hot_list")
async def get_hot_list(platform: str):
    """
    获取指定平台的热榜数据
    
    Args:
        platform: 平台名称，如zhihu、weibo、bilibili等
    
    Returns:
        code: 状态码
        message: 消息
        title: 热榜标题
        subtitle: 热榜副标题
        data: 热榜数据列表
    """
    result = await fetch_data(f"{BASE_URL}/{platform}")
    return result

@dailyhot_app.get("/zhihu", response_model=HotListResponse, operation_id="get_zhihu_hot")
async def get_zhihu_hot():
    """
    获取知乎热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("zhihu")

@dailyhot_app.get("/weibo", response_model=HotListResponse, operation_id="get_weibo_hot")
async def get_weibo_hot():
    """
    获取微博热搜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weibo")

@dailyhot_app.get("/bilibili", response_model=HotListResponse, operation_id="get_bilibili_hot")
async def get_bilibili_hot():
    """
    获取B站热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("bilibili")

@dailyhot_app.get("/news", response_model=HotListResponse, operation_id="get_news_hot")
async def get_news_hot():
    """
    获取新闻热榜 (聚合百度、网易等新闻源)
    
    Returns:
        热榜数据
    """
    sources = ["baidu", "netease-news", "sina-news", "qq-news", "toutiao"]
    tasks = [fetch_data(f"{BASE_URL}/{source}") for source in sources]
    results = await asyncio.gather(*tasks)
    
    # 选择有效结果中的第一个返回
    for result in results:
        if result.get("code") == 200:
            return result
    
    return {"code": -1, "message": "获取新闻热榜失败"}

@dailyhot_app.get("/acfun", response_model=HotListResponse, operation_id="get_acfun_hot")
async def get_acfun_hot():
    """
    获取AcFun排行榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("acfun")

@dailyhot_app.get("/zhihu-daily", response_model=HotListResponse, operation_id="get_zhihu_daily_hot")
async def get_zhihu_daily_hot():
    """
    获取知乎日报推荐榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("zhihu-daily")

@dailyhot_app.get("/baidu", response_model=HotListResponse, operation_id="get_baidu_hot")
async def get_baidu_hot():
    """
    获取百度热搜榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("baidu")

@dailyhot_app.get("/douyin", response_model=HotListResponse, operation_id="get_douyin_hot")
async def get_douyin_hot():
    """
    获取抖音热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douyin")

@dailyhot_app.get("/kuaishou", response_model=HotListResponse, operation_id="get_kuaishou_hot")
async def get_kuaishou_hot():
    """
    获取快手热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("kuaishou")

@dailyhot_app.get("/douban-movie", response_model=HotListResponse, operation_id="get_douban_movie_hot")
async def get_douban_movie_hot():
    """
    获取豆瓣电影新片榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douban-movie")

@dailyhot_app.get("/douban-group", response_model=HotListResponse, operation_id="get_douban_group_hot")
async def get_douban_group_hot():
    """
    获取豆瓣讨论小组讨论精选
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douban-group")

@dailyhot_app.get("/tieba", response_model=HotListResponse, operation_id="get_tieba_hot")
async def get_tieba_hot():
    """
    获取百度贴吧热议榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("tieba")

@dailyhot_app.get("/sspai", response_model=HotListResponse, operation_id="get_sspai_hot")
async def get_sspai_hot():
    """
    获取少数派热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sspai")

@dailyhot_app.get("/ithome", response_model=HotListResponse, operation_id="get_ithome_hot")
async def get_ithome_hot():
    """
    获取IT之家热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ithome")

@dailyhot_app.get("/ithome-xijiayi", response_model=HotListResponse, operation_id="get_ithome_xijiayi_hot")
async def get_ithome_xijiayi_hot():
    """
    获取IT之家「喜加一」最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ithome-xijiayi")

@dailyhot_app.get("/jianshu", response_model=HotListResponse, operation_id="get_jianshu_hot")
async def get_jianshu_hot():
    """
    获取简书热门推荐
    
    Returns:
        热榜数据
    """
    return await get_hot_list("jianshu")

@dailyhot_app.get("/guokr", response_model=HotListResponse, operation_id="get_guokr_hot")
async def get_guokr_hot():
    """
    获取果壳热门文章
    
    Returns:
        热榜数据
    """
    return await get_hot_list("guokr")

@dailyhot_app.get("/thepaper", response_model=HotListResponse, operation_id="get_thepaper_hot")
async def get_thepaper_hot():
    """
    获取澎湃新闻热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("thepaper")

@dailyhot_app.get("/toutiao", response_model=HotListResponse, operation_id="get_toutiao_hot")
async def get_toutiao_hot():
    """
    获取今日头条热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("toutiao")

@dailyhot_app.get("/36kr", response_model=HotListResponse, operation_id="get_36kr_hot")
async def get_36kr_hot():
    """
    获取36氪热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("36kr")

@dailyhot_app.get("/51cto", response_model=HotListResponse, operation_id="get_51cto_hot")
async def get_51cto_hot():
    """
    获取51CTO推荐榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("51cto")

@dailyhot_app.get("/csdn", response_model=HotListResponse, operation_id="get_csdn_hot")
async def get_csdn_hot():
    """
    获取CSDN排行榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("csdn")

@dailyhot_app.get("/nodeseek", response_model=HotListResponse, operation_id="get_nodeseek_hot")
async def get_nodeseek_hot():
    """
    获取NodeSeek最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("nodeseek")

@dailyhot_app.get("/juejin", response_model=HotListResponse, operation_id="get_juejin_hot")
async def get_juejin_hot():
    """
    获取稀土掘金热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("juejin")

@dailyhot_app.get("/qq-news", response_model=HotListResponse, operation_id="get_qq_news_hot")
async def get_qq_news_hot():
    """
    获取腾讯新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("qq-news")

@dailyhot_app.get("/sina", response_model=HotListResponse, operation_id="get_sina_hot")
async def get_sina_hot():
    """
    获取新浪网热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sina")

@dailyhot_app.get("/sina-news", response_model=HotListResponse, operation_id="get_sina_news_hot")
async def get_sina_news_hot():
    """
    获取新浪新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sina-news")

@dailyhot_app.get("/netease-news", response_model=HotListResponse, operation_id="get_netease_news_hot")
async def get_netease_news_hot():
    """
    获取网易新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("netease-news")

@dailyhot_app.get("/52pojie", response_model=HotListResponse, operation_id="get_52pojie_hot")
async def get_52pojie_hot():
    """
    获取吾爱破解榜单
    
    Returns:
        热榜数据
    """
    return await get_hot_list("52pojie")

@dailyhot_app.get("/hostloc", response_model=HotListResponse, operation_id="get_hostloc_hot")
async def get_hostloc_hot():
    """
    获取全球主机交流榜单
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hostloc")

@dailyhot_app.get("/huxiu", response_model=HotListResponse, operation_id="get_huxiu_hot")
async def get_huxiu_hot():
    """
    获取虎嗅24小时
    
    Returns:
        热榜数据
    """
    return await get_hot_list("huxiu")

@dailyhot_app.get("/coolapk", response_model=HotListResponse, operation_id="get_coolapk_hot")
async def get_coolapk_hot():
    """
    获取酷安热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("coolapk")

@dailyhot_app.get("/hupu", response_model=HotListResponse, operation_id="get_hupu_hot")
async def get_hupu_hot():
    """
    获取虎扑步行街热帖
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hupu")

@dailyhot_app.get("/ifanr", response_model=HotListResponse, operation_id="get_ifanr_hot")
async def get_ifanr_hot():
    """
    获取爱范儿快讯
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ifanr")

@dailyhot_app.get("/lol", response_model=HotListResponse, operation_id="get_lol_hot")
async def get_lol_hot():
    """
    获取英雄联盟更新公告
    
    Returns:
        热榜数据
    """
    return await get_hot_list("lol")

@dailyhot_app.get("/miyoushe", response_model=HotListResponse, operation_id="get_miyoushe_hot")
async def get_miyoushe_hot():
    """
    获取米游社最新消息
    
    Returns:
        热榜数据
    """
    return await get_hot_list("miyoushe")

@dailyhot_app.get("/genshin", response_model=HotListResponse, operation_id="get_genshin_hot")
async def get_genshin_hot():
    """
    获取原神最新消息
    
    Returns:
        热榜数据
    """
    return await get_hot_list("genshin")

@dailyhot_app.get("/honkai", response_model=HotListResponse, operation_id="get_honkai_hot")
async def get_honkai_hot():
    """
    获取崩坏3最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("honkai")

@dailyhot_app.get("/starrail", response_model=HotListResponse, operation_id="get_starrail_hot")
async def get_starrail_hot():
    """
    获取崩坏：星穹铁道最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("starrail")

@dailyhot_app.get("/weread", response_model=HotListResponse, operation_id="get_weread_hot")
async def get_weread_hot():
    """
    获取微信读书飙升榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weread")

@dailyhot_app.get("/ngabbs", response_model=HotListResponse, operation_id="get_ngabbs_hot")
async def get_ngabbs_hot():
    """
    获取NGA热帖
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ngabbs")

@dailyhot_app.get("/v2ex", response_model=HotListResponse, operation_id="get_v2ex_hot")
async def get_v2ex_hot():
    """
    获取V2EX主题榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("v2ex")

@dailyhot_app.get("/hellogithub", response_model=HotListResponse, operation_id="get_hellogithub_hot")
async def get_hellogithub_hot():
    """
    获取HelloGitHub Trending
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hellogithub")

@dailyhot_app.get("/weatheralarm", response_model=HotListResponse, operation_id="get_weatheralarm_hot")
async def get_weatheralarm_hot():
    """
    获取中央气象台全国气象预警
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weatheralarm")

@dailyhot_app.get("/earthquake", response_model=HotListResponse, operation_id="get_earthquake_hot")
async def get_earthquake_hot():
    """
    获取中国地震台地震速报
    
    Returns:
        热榜数据
    """
    return await get_hot_list("earthquake")

@dailyhot_app.get("/history", response_model=HotListResponse, operation_id="get_history_hot")
async def get_history_hot():
    """
    获取历史上的今天
    
    Returns:
        热榜数据
    """
    return await get_hot_list("history")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(dailyhot_app, host="0.0.0.0", port=8002) 