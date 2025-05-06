# 天气服务 (Weather API)

提供基于城市名称或经纬度获取天气信息的API服务。

## 功能特点

- 支持通过城市名称查询天气（中国城市使用拼音）
- 支持通过经纬度查询天气
- 提供标准化的天气信息，包括温度、湿度、风速等
- 集成到MCP系统，方便统一调用

## API接口

### 通过城市名称获取天气
- 接口：`/get_weather/cityname`
- 方法：POST
- 参数：
  ```json
  {
    "cityname": "beijing"
  }
  ```
- 返回：天气信息对象

### 通过经纬度获取天气
- 接口：`/get_weather/latitude_longitude`
- 方法：POST
- 参数：
  ```json
  {
    "latitude": 39.9042,
    "longitude": 116.4074
  }
  ```
- 返回：天气信息对象

## 返回数据格式

```json
{
  "code": 0,
  "weather": {
    "cityname": "beijing",
    "weather": "晴",
    "temperature": "26°C",
    "humidity": "45%",
    "wind_speed": "3级"
  },
  "msg": "success"
}
```

## MCP调用

通过MCP协议可以统一调用天气服务：

```json
{
  "operation": "weather-sse.get_weather_cityname",
  "parameters": {
    "cityname": "shanghai"
  }
}
```

或者通过经纬度调用：

```json
{
  "operation": "weather-sse.get_weather_latitude_longitude",
  "parameters": {
    "latitude": 31.2304,
    "longitude": 121.4737
  }
}
```

## 数据来源

本服务使用公开的天气API接口获取数据，确保数据的实时性和准确性。

## 配置

天气API需要配置OpenWeatherMap API密钥才能正常工作。请按照以下步骤设置：

1. 在[OpenWeatherMap](https://openweathermap.org/)注册账号并获取API密钥
2. 将`config.example.py`复制为`config.py`
3. 在`config.py`中填入您的API密钥

注意：`config.py`文件包含敏感信息，已添加到`.gitignore`中，不会上传到GitHub。
