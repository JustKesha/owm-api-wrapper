import geopy

DEFAULT_ADDRESS_TYPES = [
    'city',
    'province',
    'town',
    'village',
    'hamlet',
    
    'islet',
    'county',
    ]

configurated = False
geolocator:geopy.geocoders.Nominatim = None

def configurate(user_agent:str):
    global geolocator, configurated

    geolocator = geopy.geocoders.Nominatim(user_agent=user_agent)
    
    configurated = True

def request_raw_locations_data(search_input:str, address_types:list=DEFAULT_ADDRESS_TYPES) -> list:
    global geolocator

    if not configurated:
        raise Exception('Trying to call geocode.api.request_raw_locations_data(...), but geocode.api was not configurated. Make sure to first run geocode.api.configurate(...).')

    if search_input == None or len(search_input) == 0:
        return []
    
    results = geolocator.geocode(search_input, language='en-us', addressdetails=True, extratags=True, namedetails=True, exactly_one=False)

    if results == None or len(results) == 0:
        return []
    
    raw_results = list(map(lambda loc: loc.raw, results))
    raw_results = sorted(raw_results, key=lambda raw_loc: raw_loc['importance'], reverse=True)

    if len(address_types) != 0:
        raw_results = [location for location in raw_results if location['addresstype'] in address_types]
    
    return raw_results