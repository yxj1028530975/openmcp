from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
import httpx
import asyncio
import os
from common.server import server_app


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


@server_app.get("/hot/{platform}", response_model=HotListResponse, operation_id="get_hot_list", tags=["热榜通用"])
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
    result = await fetch_data(f"{BASE_URL}/{platform}?limit=10")
    return result

@server_app.get("/zhihu", response_model=HotListResponse, operation_id="get_zhihu_hot", tags=["社交媒体"])
async def get_zhihu_hot():
    """
    获取知乎热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("zhihu")

@server_app.get("/weibo", response_model=HotListResponse, operation_id="get_weibo_hot", tags=["社交媒体"])
async def get_weibo_hot():
    """
    获取微博热搜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weibo")

@server_app.get("/bilibili", response_model=HotListResponse, operation_id="get_bilibili_hot", tags=["视频平台"])
async def get_bilibili_hot():
    """
    获取B站热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("bilibili")

@server_app.get("/news", response_model=HotListResponse, operation_id="get_news_hot", tags=["新闻资讯"])
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

@server_app.get("/acfun", response_model=HotListResponse, operation_id="get_acfun_hot", tags=["视频平台"])
async def get_acfun_hot():
    """
    获取AcFun排行榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("acfun")

@server_app.get("/zhihu-daily", response_model=HotListResponse, operation_id="get_zhihu_daily_hot", tags=["社交媒体"])
async def get_zhihu_daily_hot():
    """
    获取知乎日报推荐榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("zhihu-daily")

@server_app.get("/baidu", response_model=HotListResponse, operation_id="get_baidu_hot", tags=["搜索引擎"])
async def get_baidu_hot():
    """
    获取百度热搜榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("baidu")

@server_app.get("/douyin", response_model=HotListResponse, operation_id="get_douyin_hot", tags=["视频平台"])
async def get_douyin_hot():
    """
    获取抖音热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douyin")

@server_app.get("/kuaishou", response_model=HotListResponse, operation_id="get_kuaishou_hot", tags=["视频平台"])
async def get_kuaishou_hot():
    """
    获取快手热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("kuaishou")

@server_app.get("/douban-movie", response_model=HotListResponse, operation_id="get_douban_movie_hot", tags=["娱乐影视"])
async def get_douban_movie_hot():
    """
    获取豆瓣电影新片榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douban-movie")

@server_app.get("/douban-group", response_model=HotListResponse, operation_id="get_douban_group_hot", tags=["社交媒体"])
async def get_douban_group_hot():
    """
    获取豆瓣讨论小组讨论精选
    
    Returns:
        热榜数据
    """
    return await get_hot_list("douban-group")

@server_app.get("/tieba", response_model=HotListResponse, operation_id="get_tieba_hot", tags=["社交媒体"])
async def get_tieba_hot():
    """
    获取百度贴吧热议榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("tieba")

@server_app.get("/sspai", response_model=HotListResponse, operation_id="get_sspai_hot", tags=["科技数码"])
async def get_sspai_hot():
    """
    获取少数派热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sspai")

@server_app.get("/ithome", response_model=HotListResponse, operation_id="get_ithome_hot", tags=["科技数码"])
async def get_ithome_hot():
    """
    获取IT之家热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ithome")

@server_app.get("/ithome-xijiayi", response_model=HotListResponse, operation_id="get_ithome_xijiayi_hot", tags=["科技数码"])
async def get_ithome_xijiayi_hot():
    """
    获取IT之家「喜加一」最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ithome-xijiayi")

@server_app.get("/jianshu", response_model=HotListResponse, operation_id="get_jianshu_hot", tags=["内容平台"])
async def get_jianshu_hot():
    """
    获取简书热门推荐
    
    Returns:
        热榜数据
    """
    return await get_hot_list("jianshu")

@server_app.get("/guokr", response_model=HotListResponse, operation_id="get_guokr_hot", tags=["内容平台"])
async def get_guokr_hot():
    """
    获取果壳热门文章
    
    Returns:
        热榜数据
    """
    return await get_hot_list("guokr")

@server_app.get("/thepaper", response_model=HotListResponse, operation_id="get_thepaper_hot", tags=["新闻资讯"])
async def get_thepaper_hot():
    """
    获取澎湃新闻热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("thepaper")

@server_app.get("/toutiao", response_model=HotListResponse, operation_id="get_toutiao_hot", tags=["新闻资讯"])
async def get_toutiao_hot():
    """
    获取今日头条热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("toutiao")

@server_app.get("/36kr", response_model=HotListResponse, operation_id="get_36kr_hot", tags=["科技数码"])
async def get_36kr_hot():
    """
    获取36氪热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("36kr")

@server_app.get("/51cto", response_model=HotListResponse, operation_id="get_51cto_hot", tags=["技术开发"])
async def get_51cto_hot():
    """
    获取51CTO推荐榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("51cto")

@server_app.get("/csdn", response_model=HotListResponse, operation_id="get_csdn_hot", tags=["技术开发"])
async def get_csdn_hot():
    """
    获取CSDN排行榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("csdn")

@server_app.get("/nodeseek", response_model=HotListResponse, operation_id="get_nodeseek_hot", tags=["技术开发"])
async def get_nodeseek_hot():
    """
    获取NodeSeek最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("nodeseek")

@server_app.get("/juejin", response_model=HotListResponse, operation_id="get_juejin_hot", tags=["技术开发"])
async def get_juejin_hot():
    """
    获取稀土掘金热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("juejin")

@server_app.get("/qq-news", response_model=HotListResponse, operation_id="get_qq_news_hot", tags=["新闻资讯"])
async def get_qq_news_hot():
    """
    获取腾讯新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("qq-news")

@server_app.get("/sina", response_model=HotListResponse, operation_id="get_sina_hot", tags=["新闻资讯"])
async def get_sina_hot():
    """
    获取新浪网热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sina")

@server_app.get("/sina-news", response_model=HotListResponse, operation_id="get_sina_news_hot", tags=["新闻资讯"])
async def get_sina_news_hot():
    """
    获取新浪新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("sina-news")

@server_app.get("/netease-news", response_model=HotListResponse, operation_id="get_netease_news_hot", tags=["新闻资讯"])
async def get_netease_news_hot():
    """
    获取网易新闻热点榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("netease-news")

@server_app.get("/52pojie", response_model=HotListResponse, operation_id="get_52pojie_hot", tags=["技术开发"])
async def get_52pojie_hot():
    """
    获取吾爱破解榜单
    
    Returns:
        热榜数据
    """
    return await get_hot_list("52pojie")

@server_app.get("/hostloc", response_model=HotListResponse, operation_id="get_hostloc_hot", tags=["技术开发"])
async def get_hostloc_hot():
    """
    获取全球主机交流榜单
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hostloc")

@server_app.get("/huxiu", response_model=HotListResponse, operation_id="get_huxiu_hot", tags=["科技数码"])
async def get_huxiu_hot():
    """
    获取虎嗅24小时
    
    Returns:
        热榜数据
    """
    return await get_hot_list("huxiu")

@server_app.get("/coolapk", response_model=HotListResponse, operation_id="get_coolapk_hot", tags=["科技数码"])
async def get_coolapk_hot():
    """
    获取酷安热榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("coolapk")

@server_app.get("/hupu", response_model=HotListResponse, operation_id="get_hupu_hot", tags=["社交媒体"])
async def get_hupu_hot():
    """
    获取虎扑步行街热帖
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hupu")

@server_app.get("/ifanr", response_model=HotListResponse, operation_id="get_ifanr_hot", tags=["科技数码"])
async def get_ifanr_hot():
    """
    获取爱范儿快讯
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ifanr")

@server_app.get("/lol", response_model=HotListResponse, operation_id="get_lol_hot", tags=["游戏动漫"])
async def get_lol_hot():
    """
    获取英雄联盟更新公告
    
    Returns:
        热榜数据
    """
    return await get_hot_list("lol")

@server_app.get("/miyoushe", response_model=HotListResponse, operation_id="get_miyoushe_hot", tags=["游戏动漫"])
async def get_miyoushe_hot():
    """
    获取米游社最新消息
    
    Returns:
        热榜数据
    """
    return await get_hot_list("miyoushe")

@server_app.get("/genshin", response_model=HotListResponse, operation_id="get_genshin_hot", tags=["游戏动漫"])
async def get_genshin_hot():
    """
    获取原神最新消息
    
    Returns:
        热榜数据
    """
    return await get_hot_list("genshin")

@server_app.get("/honkai", response_model=HotListResponse, operation_id="get_honkai_hot", tags=["游戏动漫"])
async def get_honkai_hot():
    """
    获取崩坏3最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("honkai")

@server_app.get("/starrail", response_model=HotListResponse, operation_id="get_starrail_hot", tags=["游戏动漫"])
async def get_starrail_hot():
    """
    获取崩坏：星穹铁道最新动态
    
    Returns:
        热榜数据
    """
    return await get_hot_list("starrail")

@server_app.get("/weread", response_model=HotListResponse, operation_id="get_weread_hot", tags=["内容平台"])
async def get_weread_hot():
    """
    获取微信读书飙升榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weread")

@server_app.get("/ngabbs", response_model=HotListResponse, operation_id="get_ngabbs_hot", tags=["游戏动漫"])
async def get_ngabbs_hot():
    """
    获取NGA热帖
    
    Returns:
        热榜数据
    """
    return await get_hot_list("ngabbs")

@server_app.get("/v2ex", response_model=HotListResponse, operation_id="get_v2ex_hot", tags=["技术开发"])
async def get_v2ex_hot():
    """
    获取V2EX主题榜
    
    Returns:
        热榜数据
    """
    return await get_hot_list("v2ex")

@server_app.get("/hellogithub", response_model=HotListResponse, operation_id="get_hellogithub_hot", tags=["技术开发"])
async def get_hellogithub_hot():
    """
    获取HelloGitHub Trending
    
    Returns:
        热榜数据
    """
    return await get_hot_list("hellogithub")

@server_app.get("/weatheralarm", response_model=HotListResponse, operation_id="get_weatheralarm_hot", tags=["生活服务"])
async def get_weatheralarm_hot():
    """
    获取中央气象台全国气象预警
    
    Returns:
        热榜数据
    """
    return await get_hot_list("weatheralarm")

@server_app.get("/earthquake", response_model=HotListResponse, operation_id="get_earthquake_hot", tags=["生活服务"])
async def get_earthquake_hot():
    """
    获取中国地震台地震速报
    
    Returns:
        热榜数据
    """
    return await get_hot_list("earthquake")

@server_app.get("/history", response_model=HotListResponse, operation_id="get_history_hot", tags=["生活服务"])
async def get_history_hot():
    """
    获取历史上的今天
    
    Returns:
        热榜数据
    """
    return await get_hot_list("history")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server_app, host="0.0.0.0", port=8002) 