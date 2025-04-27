from fastapi import FastAPI
from pydantic import BaseModel
from .utils import format_alert, get_weather_from_cityname, get_weather_from_latitude_longitude
import uvicorn

weather_app = FastAPI(title="天气信息API", description="通过城市名称（中国城市使用拼音）或经纬度获取天气信息")

class CityName(BaseModel):
    cityname: str

class CityLatLon(BaseModel):
    latitude: float
    longitude: float

class Weather(BaseModel):
    cityname: str
    weather: str
    temperature: str
    humidity: str
    wind_speed: str

class WeatherResponse(BaseModel):
    code: int
    weather: Weather | None = None
    msg: str

@weather_app.post("/get_weather/cityname", response_model=WeatherResponse, operation_id="get_weather_cityname")
async def get_weather_cityname(city: CityName):
    """
    通过城市名称（中国城市使用拼音）获取天气信息

    Args:
        cityname: 城市名称（中国城市使用拼音）
    
    Returns:
        code: 0 成功 -1 失败
        weather: 天气信息
        msg: 成功或失败信息
    """
    weather_data = await get_weather_from_cityname(city.cityname)
    if weather_data:
        weather_info = format_alert(weather_data)
        if "error" in weather_info:
            return {"code": -1, "msg": weather_info.get("error", "Failed to fetch weather data")}
        return {"code": 0, "weather": Weather(**weather_info), "msg": "success"}
    else:
        return {"code": -1, "msg": "Failed to fetch weather data"}

@weather_app.post("/get_weather/latitude_longitude", response_model=WeatherResponse, operation_id="get_weather_latitude_longitude")
async def get_weather_latitude_longitude(citylatlon: CityLatLon):
    """
    通过经纬度获取天气信息

    Args:
        latitude: 纬度
        longitude: 经度

    Returns:
        code: 0 成功 -1 失败
        weather: 天气信息
        msg: 成功或失败信息
    """
    weather_data = await get_weather_from_latitude_longitude(citylatlon.latitude, citylatlon.longitude)
    if weather_data:
        weather_info = format_alert(weather_data)
        if "error" in weather_info:
            return {"code": -1, "msg": weather_info.get("error", "Failed to fetch weather data")}
        return {"code": 0, "weather": Weather(**weather_info), "msg": "success"}
    else:
        return {"code": -1, "msg": "Failed to fetch weather data"}

if __name__ == "__main__":
    uvicorn.run(weather_app, host='0.0.0.0', port=8000)