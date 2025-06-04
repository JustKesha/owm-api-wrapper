from importlib import resources
import json

PACKAGE_NAME = 'weather'
DATA_FILE_NAME = 'data.json'
ENGLISH_FILE_NAME = 'english.json'

with resources.open_text(PACKAGE_NAME, DATA_FILE_NAME) as file:
    """
    colors_by_temperature

    Should be a sorted array (from lower to higher temps);
    Where each element (except for the last one not having a max temp value)
    contains an inclusive max temp value in c (as max_c) and a color in hex (as hex).

    colors_by_condition

    Should have keys set as weather condition codes from,
    https://openweathermap.org/weather-condition;
    And values to those keys as hex colors.
    """
    DATA = json.load(file)

with resources.open_text(PACKAGE_NAME, ENGLISH_FILE_NAME) as file:
    ENGLISH = json.load(file)