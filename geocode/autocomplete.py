import importlib.resources
import json

CURRENT_PACKAGE_NAME = 'geocode'
AUTOCOMPLETE_DATA_FILE_NAME = 'autocomplete.json'

data:dict

with importlib.resources.open_text(CURRENT_PACKAGE_NAME, AUTOCOMPLETE_DATA_FILE_NAME) as file:
    data = json.load(file)

def autocomplete(input:str) -> str:
    input = input.lower()

    return data[input] if input in data.keys() else input
