from .autocomplete import autocomplete
from .api import request_raw_locations_data
from .format import Location, format_raw_locations_data, format_raw_location_data

def get_locations(search_input:str, use_autocomplete:bool=True) -> list:
    if use_autocomplete:
        search_input = autocomplete(search_input)

    try:
        raw_locations = request_raw_locations_data(search_input)
    except Exception as error:
        raise error
    
    if len(raw_locations) == 0:
        return []
    
    locations = format_raw_locations_data(raw_locations)

    return locations

def get_location(search_input:str, use_autocomplete:bool=True) -> Location:
    if use_autocomplete:
        search_input = autocomplete(search_input)
    
    try:
        raw_locations = request_raw_locations_data(search_input)
    except Exception as error:
        raise error

    if len(raw_locations) == 0:
        return None
    
    location = format_raw_location_data(raw_locations[0])

    return location