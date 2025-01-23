import json
import pkgutil
from enum import Enum
from typing import Union
from io import BytesIO

from .globals import PACKAGE_NAME

ICON_SETS_DIR = 'icons'
ICON_SET_INDEX_FILE_NAME = 'index.json'

# NOTE Dont forget to update this when changing icon sets list
class IconSets(Enum):
    # Values must be names of icon set directories
    Dev = 'dev'
    Microsoft3D = 'microsoft'

    DEFAULT = Dev

icon_sets_data = {}

def get_icon_set_path(icon_set:IconSets, separator:str='/'):
    return separator.join([
        ICON_SETS_DIR,
        icon_set.value,
    ])

def get_icon_set_data(icon_set:IconSets) -> dict:
    # Returns data from the index file of chosen icon set as dict
    # Can raise the same errors as importlib.resources.open_text, json.load

    path = '/'.join([
        get_icon_set_path(icon_set),
        ICON_SET_INDEX_FILE_NAME, 
    ])

    try:
        # Using importlib.resources only allows for import from a package dir
        byte = pkgutil.get_data(PACKAGE_NAME, path)
        data = json.loads(byte)
    except:
        raise
    
    return data

def get_icon_sets_data() -> dict:
    # Returns a "icon set dir name" to "icon set json data" type of dict
    # Can raise the same errors as get_icon_set_data

    out = {}

    for icon_set in IconSets:
        try:
            data = get_icon_set_data(icon_set)
        except:
            raise

        out[icon_set.value] = data

    return out

def update_icon_sets_data() -> None:
    global icon_sets_data

    icon_sets_data = get_icon_sets_data()


def is_icon_in_set(
        icon_set:IconSets,
        icon_name:str,
        icon_index:int=0
        ) -> bool:
    
    icon_set_data:dict = icon_sets_data[icon_set.value]

    if not icon_name in icon_set_data.keys():
        return False
    
    return icon_index >= 0 and icon_index < len(icon_set_data[icon_name])

def get_icon_file_name(
        icon_set:IconSets,
        icon_name:str,
        icon_index:int=0
        ) -> Union[str, None]:
    if not is_icon_in_set(icon_set, icon_name, icon_index):
        return None
    
    return icon_sets_data[icon_set.value][icon_name][icon_index]

def get_icon_bytes(
        icon_name:str,
        icon_index:int=0,
        icon_set:IconSets=IconSets.DEFAULT,

        retry_default_set:bool=True,
        retry_lower_index:bool=True,
        ) -> Union[bytes, None]:
    # Returns byte data of the icon image file or None
    # If retry_default_set true will retry using the default set if icon wasnt found
    # If retry_lower_index true will retry with a lower index if no icon with given index found

    if not is_icon_in_set(icon_set, icon_name):
        
        if retry_default_set and not icon_set is IconSets.DEFAULT:
            return get_icon_bytes(icon_name, icon_index)
        else:
            return None

    if not is_icon_in_set(icon_set, icon_name, icon_index):
        
        if retry_lower_index:
            icon_index = len(icon_sets_data[icon_set.value][icon_name]) - 1
        else:
            return None
    
    
    path = '/'.join([
        get_icon_set_path(icon_set),
        get_icon_file_name(icon_set, icon_name, icon_index),
    ])

    try:
        return pkgutil.get_data(PACKAGE_NAME, path)
    except:
        return None

def get_icon_bytes_io(
        icon_name:str,
        icon_index:int=0,
        icon_set:IconSets=IconSets.DEFAULT,

        retry_default_set:bool=True,
        retry_lower_index:bool=True,
        ) -> Union[BytesIO, None]:
    
    try:
        data = get_icon_bytes(
            icon_name,
            icon_index,
            icon_set,

            retry_default_set=retry_default_set,
            retry_lower_index=retry_lower_index,
            )
    except:
        raise
    
    if not data:
        return None

    return BytesIO(data)

update_icon_sets_data()