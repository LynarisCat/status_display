import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from typing import Dict, List

# sunny -> 0; cloudy -> 1; rain/stormy -> 2; wtf -> -1
def get_cloud_index(code: int) -> int:
    
    if code in range(0,2):
        return 0
    elif code in range(3, 70):
        return 1
    elif code in range(71, 100):
        return 2
    else:
        return -1


# --- Mostly from the official openmetro docs ---

def get_weather() -> List[Dict[str, int]]:
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.59016,
        "longitude": 12.025504,
        "daily": ["temperature_2m_max", "weather_code"],
        "timezone": "Europe/Berlin",
        "past_days": 0,
        "forecast_days": 2,
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy().tolist()
    daily_weather_code = daily.Variables(1).ValuesAsNumpy().tolist()

    weather=[ {"cloud_code": get_cloud_index(daily_weather_code[0]), "temp": daily_temperature_2m_max[0]}, {"cloud_code": get_cloud_index(daily_weather_code[1]), "temp": daily_temperature_2m_max[1]}]

    # print(weather)
    

    return weather
