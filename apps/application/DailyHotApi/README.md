# DailyHotApi MCP

本模块将 [今日热榜 API](https://github.com/imsyy/DailyHotApi) 集成到 FastApiMCP 系统中，提供各大热门平台的热榜数据。

## 功能特点

- 支持知乎、微博、B站等50多个平台的热榜数据
- 通过MCP机制提供API调用
- 完全基于原项目的API能力
- 提供聚合新闻热榜功能

## 部署方式

1. 首先部署原始DailyHotApi服务：

```bash
cd apps/DailyHotApi
docker-compose up -d
```

2. 安装必要的依赖：

```bash
pip install httpx
```

## API接口

### 获取所有可用热榜
- 接口：`/routes`
- 方法：GET
- 返回：所有支持的热榜平台列表

### 获取指定平台热榜
- 接口：`/hot/{platform}`
- 方法：GET
- 参数：platform - 平台名称
- 返回：该平台的热榜数据

### 常用平台直接接口
- 知乎热榜：`/zhihu`
- 微博热搜：`/weibo`
- B站热榜：`/bilibili`
- 新闻热榜(聚合)：`/news`

## 支持的平台列表

| 站点 | 类别 | 调用名称 | 接口地址 |
|------|------|----------|----------|
| 哔哩哔哩 | 热门榜 | bilibili | /bilibili |
| AcFun | 排行榜 | acfun | /acfun |
| 微博 | 热搜榜 | weibo | /weibo |
| 知乎 | 热榜 | zhihu | /zhihu |
| 知乎日报 | 推荐榜 | zhihu-daily | /zhihu-daily |
| 百度 | 热搜榜 | baidu | /baidu |
| 抖音 | 热点榜 | douyin | /douyin |
| 快手 | 热点榜 | kuaishou | /kuaishou |
| 豆瓣电影 | 新片榜 | douban-movie | /douban-movie |
| 豆瓣讨论小组 | 讨论精选 | douban-group | /douban-group |
| 百度贴吧 | 热议榜 | tieba | /tieba |
| 少数派 | 热榜 | sspai | /sspai |
| IT之家 | 热榜 | ithome | /ithome |
| IT之家「喜加一」 | 最新动态 | ithome-xijiayi | /ithome-xijiayi |
| 简书 | 热门推荐 | jianshu | /jianshu |
| 果壳 | 热门文章 | guokr | /guokr |
| 澎湃新闻 | 热榜 | thepaper | /thepaper |
| 今日头条 | 热榜 | toutiao | /toutiao |
| 36 氪 | 热榜 | 36kr | /36kr |
| 51CTO | 推荐榜 | 51cto | /51cto |
| CSDN | 排行榜 | csdn | /csdn |
| NodeSeek | 最新动态 | nodeseek | /nodeseek |
| 稀土掘金 | 热榜 | juejin | /juejin |
| 腾讯新闻 | 热点榜 | qq-news | /qq-news |
| 新浪网 | 热榜 | sina | /sina |
| 新浪新闻 | 热点榜 | sina-news | /sina-news |
| 网易新闻 | 热点榜 | netease-news | /netease-news |
| 吾爱破解 | 榜单 | 52pojie | /52pojie |
| 全球主机交流 | 榜单 | hostloc | /hostloc |
| 虎嗅 | 24小时 | huxiu | /huxiu |
| 酷安 | 热榜 | coolapk | /coolapk |
| 虎扑 | 步行街热帖 | hupu | /hupu |
| 爱范儿 | 快讯 | ifanr | /ifanr |
| 英雄联盟 | 更新公告 | lol | /lol |
| 米游社 | 最新消息 | miyoushe | /miyoushe |
| 原神 | 最新消息 | genshin | /genshin |
| 崩坏3 | 最新动态 | honkai | /honkai |
| 崩坏：星穹铁道 | 最新动态 | starrail | /starrail |
| 微信读书 | 飙升榜 | weread | /weread |
| NGA | 热帖 | ngabbs | /ngabbs |
| V2EX | 主题榜 | v2ex | /v2ex |
| HelloGitHub | Trending | hellogithub | /hellogithub |
| 中央气象台 | 全国气象预警 | weatheralarm | /weatheralarm |
| 中国地震台 | 地震速报 | earthquake | /earthquake |
| 历史上的今天 | 月-日 | history | /history |

## MCP调用示例

通过MCP协议统一调用热榜数据：

```json
{
  "operation": "dailyhot-sse.get_zhihu_hot",
  "parameters": {}
}
```

或者获取指定平台的热榜：

```json
{
  "operation": "dailyhot-sse.get_hot_list",
  "parameters": {
    "platform": "bilibili"
  }
}
```

## 依赖关系

本模块依赖于原始的DailyHotApi服务，需要确保该服务正确运行在配置的端口上（默认为6688）。

## 数据来源

数据来源于各大平台官方，由原始DailyHotApi项目提供数据获取能力。 