import json

# TODO Switch to using Nominatim/OpenStreetMap api with no geopy
import geopy # pip install geopy
# from geopy.geocoders import Nominatim

DEFAULT_ADDRESS_TYPES = ['city','village','hamlet']

configurated = False
geolocator:geopy.geocoders.Nominatim = None

def configurate(user_agent:str):
    global geolocator, autocomplete_data, configurated

    geolocator = geopy.geocoders.Nominatim(user_agent=user_agent)

    with open('./geocode/autocomplete.json', 'r', encoding='utf-8') as file:
        autocomplete_data = json.load(file)
    
    configurated = True

def request_raw_locations_data(search_input:str, address_types:list=DEFAULT_ADDRESS_TYPES) -> list:
    global geolocator

    if not configurated:
        raise Exception('Trying to call geocode.api.request_raw_locations_data(...), but geocode.api was not configurated. Make sure to first run geocode.api.configurate(...).')

    if search_input == None or len(search_input) == 0:
        return []
    
    # Docs https://geopy.readthedocs.io/en/stable/index.html#geopy.geocoders.Nominatim.geocode
    results = geolocator.geocode(search_input, language='en-us', addressdetails=True, extratags=True, namedetails=True, exactly_one=False)

    if results == None or len(results) == 0:
        return []
    
    # To raw api results
    raw_results = list(map(lambda loc: loc.raw, results))

    # Sort by importance
    raw_results = sorted(raw_results, key=lambda raw_loc: raw_loc['importance'], reverse=True)

    # If address_types not empty, only include results matching any of address_types
    if len(address_types) != 0:
        raw_results = [location for location in raw_results if location['addresstype'] in address_types]

    return raw_results