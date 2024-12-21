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
    # Values should be the names of icon set directories
    Paint = 'paint'

    DEFAULT = Paint

# Working with icon sets data

icon_sets_data = {}

def get_icon_set_path(icon_set:IconSets, separator:str='/'):
    return separator.join([
        ICON_SETS_DIR,
        icon_set.value,
    ])

# FIXME Im not sure its a good practice
# What if intead itd take a str or IconSets / str
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

update_icon_sets_data()

# Working with icon files

def is_icon_in_set(icon_set:IconSets, icon_name:str) -> bool:
    return icon_name in icon_sets_data[icon_set.value].keys()

def get_icon_file_name(icon_set:IconSets, icon_name:str) -> Union[str, None]:
    if not is_icon_in_set(icon_set, icon_name):
        return None
    
    return icon_sets_data[icon_set.value][icon_name]

def get_icon_bytes(
        icon_name:str,
        icon_set:IconSets=IconSets.DEFAULT,
        retry_with_default:bool=True
        ) -> Union[bytes, None]:
    # Returns byte data of the icon image file or None
    # If retry_with_default true will rerun using the default set if icon wasnt found
    
    if not is_icon_in_set(icon_set, icon_name):
        if not icon_set is IconSets.DEFAULT and retry_with_default:
            return get_icon_bytes(icon_name)
        else:
            return None
    
    path = '/'.join([
        get_icon_set_path(icon_set),
        get_icon_file_name(icon_set, icon_name),
    ])

    try:
        return pkgutil.get_data(PACKAGE_NAME, path)
    except:
        return None

def get_icon_bytes_io(
        icon_name:str,
        icon_set:IconSets=IconSets.DEFAULT,
        retry_with_default:bool=True
        ) -> Union[BytesIO, None]:
    
    try:
        data = get_icon_bytes(icon_name, icon_set, retry_with_default)
    except:
        raise
    
    if not data:
        return None

    return BytesIO(data)