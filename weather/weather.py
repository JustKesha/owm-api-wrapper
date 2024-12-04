from .api import request_data
from .format import Weather, format_data

async def get_weather(lat:float=0, lon:float=0, test:bool=False) -> Weather:
    try:
        raw_weather = await request_data(test=True) if test else await request_data(lat, lon)
    except Exception as e:
        raise e

    return format_data(raw_weather)