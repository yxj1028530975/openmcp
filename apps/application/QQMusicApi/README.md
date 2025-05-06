# QQ音乐API接口

基于[QQMusicApi](https://github.com/luren-dc/QQMusicApi)的FastAPI封装，提供QQ音乐API的HTTP接口。

## 安装

```bash
# 安装依赖
pip install fastapi uvicorn qqmusic-api-python
```

## 运行服务

```bash
# 直接运行
python QQMusic_api.py

# 或使用uvicorn运行
uvicorn QQMusic_api:qqmusic_app --host 0.0.0.0 --port 8001
```

## API接口

### 二维码登录

#### 1. 获取二维码

```
GET /login/qrcode/{login_type}
```

参数：
- `login_type`：登录类型，可选 `qq` 或 `wx`

响应示例：

```json
{
  "code": 200,
  "message": "获取二维码成功",
  "qr_id": "xyz123...",
  "qr_image": "base64编码的图片数据..."
}
```

#### 2. 检查二维码状态

```
GET /login/check/{qr_id}
```

参数：
- `qr_id`：二维码ID，从获取二维码接口获得

响应示例（等待扫描）：

```json
{
  "code": 100,
  "message": "等待扫描",
  "status": "WAITING"
}
```

响应示例（已扫描，等待确认）：

```json
{
  "code": 201,
  "message": "二维码已扫描，等待确认",
  "status": "SCAN"
}
```

响应示例（登录成功）：

```json
{
  "code": 200,
  "message": "登录成功",
  "status": "DONE",
  "musicid": "12345",
  "credential": {
    "musicid": "12345",
    "uin": "xxx",
    "...": "更多凭证信息"
  }
}
```

### 搜索接口

#### 1. 综合搜索

```
GET /search/general?keyword={keyword}&page={page}&highlight={highlight}
```

参数：
- `keyword`：搜索关键词
- `page`：页码，默认为1
- `highlight`：是否高亮结果，默认为false

#### 2. 按类型搜索

```
GET /search/by_type?keyword={keyword}&search_type={search_type}&page={page}&num={num}&highlight={highlight}
```

参数：
- `keyword`：搜索关键词
- `search_type`：搜索类型，可选值：
  - `song`：歌曲
  - `album`：专辑
  - `singer`：歌手
  - `playlist`：播放列表
  - `mv`：MV
  - `lyric`：歌词
  - `user`：用户
- `page`：页码，默认为1
- `num`：每页数量，默认为20
- `highlight`：是否高亮结果，默认为false

#### 3. 快速搜索

```
GET /search/quick?keyword={keyword}
```

参数：
- `keyword`：搜索关键词

### 健康检查

```
GET /health
```

响应示例：

```json
{
  "status": "ok"
}
```

## 使用示例

### 获取QQ登录二维码

```bash
curl -X GET "http://localhost:8001/login/qrcode/qq"
```

### 检查二维码状态

```bash
curl -X GET "http://localhost:8001/login/check/YOUR_QR_ID"
```

### 搜索周杰伦的歌曲

```bash
curl -X GET "http://localhost:8001/search/by_type?keyword=周杰伦&search_type=song&num=20"
```

## 注意事项

- 本接口仅供学习和研究使用，请尊重版权，支持正版。
- 登录功能目前仅支持二维码登录方式。
- 二维码有效期有限，过期后需要重新获取。
