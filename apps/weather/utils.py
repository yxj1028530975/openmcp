from typing import Any
import httpx

# 常量
NWS_API_BASE = "https://api.openweathermap.org/data/2.5/weather"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
API_KEY = "0c1ad5389997bb1bdf3ae117d28870e7"
# 温度单位转换，将开尔文转化为摄氏度
def kelvin_to_celsius(kelvin: float) -> float:
    return kelvin - 273.15

async def get_weather_from_cityname(cityname: str) -> dict[str, Any] | None:
    """向openweathermap发送请求并进行适当的错误处理。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    params = {
        "q": cityname,
        "appid": API_KEY
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NWS_API_BASE, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def get_weather_from_latitude_longitude(latitude: float, longitude: float) -> dict[str, Any] | None:
    """向openweathermap发送请求并进行适当的错误处理。"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": "{API KEY}"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(NWS_API_BASE, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> dict:
    """将接口返回的天气信息进行格式化"""
    if feature["cod"] == 404:
        return {"cityname": "", "weather": "", "temperature": "", "humidity": "", "wind_speed": "", "error": "参数异常，请确认城市名称是否正确。"}
    elif feature["cod"] == 401:
        return {"cityname": "", "weather": "", "temperature": "", "humidity": "", "wind_speed": "", "error": "API key 异常，请确认API key是否正确。"}
    elif feature["cod"] == 200:
        return {
            "cityname": feature.get('name', 'Unknown'),
            "weather": feature.get('weather', [{}])[0].get('description', 'Unknown'),
            "temperature": f"{kelvin_to_celsius(feature.get('main', {}).get('temp', 0)):.2f}°C",
            "humidity": f"{feature.get('main', {}).get('humidity', 0)}%",
            "wind_speed": f"{feature.get('wind', {}).get('speed', 0):.2f} m/s"
        }
    else:
        return {"cityname": "", "weather": "", "temperature": "", "humidity": "", "wind_speed": "", "error": "未知错误，请稍后再试。"}