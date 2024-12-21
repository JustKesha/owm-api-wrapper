from utils import convert
from . import globals

DEFAULT_HEX_BY_CONDITION_OUTPUT = '#313338'

def get_hex_by_temperature(c:float) -> str:
    arr = globals.DATA['colors_by_temperature']
    max_i = len(arr) - 1

    for i in range(max_i + 1):
        if i == max_i or c <= arr[i]['max_c']:
            return arr[i]['hex']

def does_condition_have_hex(weather_code:int) -> bool:
    return str(weather_code) in globals.DATA['colors_by_condition']

def get_hex_by_condition(weather_code:int) -> str:
    if not does_condition_have_hex(weather_code):
        return DEFAULT_HEX_BY_CONDITION_OUTPUT
    
    return globals.DATA['colors_by_condition'][str(weather_code)]

def get_weather_hex(weather_code:int, temp_c:float):
    if does_condition_have_hex(weather_code):
        return get_hex_by_condition(weather_code)
    
    return get_hex_by_temperature(temp_c)

class Color():
    def __init__(self, weather_code:int, temp_c:float) -> None:
        self.hex = get_weather_hex(
            weather_code = weather_code,
            temp_c = temp_c,
            )
        self.dex = convert.hex_to_dex(self.hex)