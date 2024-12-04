import importlib
import json

import requests

configurated = False
example_data:dict

with importlib.resources.open_text("weather", "raw-test-data.json") as file: # Uses utf-8 encoding by default
    example_data = json.load(file)

def configurate(base_url:str, key:str):
    global BASE_URL, KEY, configurated

    BASE_URL = base_url
    KEY = key

    configurated = True

async def request_data(lat:float=0, lon:float=0, test:bool=False) -> dict:
    if not configurated:
        raise Exception('Trying to use weather.api.request_data(...), but the module was not configurated. Make sure to first run weather.api.configurate(...).')
    
    if test:
        return example_data

    request_url = BASE_URL + f'?lat={lat}&lon={lon}&appid={KEY}'

    print(request_url)

    try:
        response_raw = requests.get(request_url)
    except Exception as error:
        raise error
    
    response = response_raw.json()

    return response
