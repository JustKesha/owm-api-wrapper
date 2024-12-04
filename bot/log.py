class MessageTypes():
    PROC = 0
    INFO = 1
    WARN = 2

class FilterTypes():
    # TODO Add filters
    NONE = 0

prefixes = {
    MessageTypes.PROC: '/',
    MessageTypes.INFO: '?',
    MessageTypes.WARN: '!',
}

active = True
allowed_message_types = []

name = 'discord'
name_separator = ': '
ongoing_postfix = '...'

def set_active(value:bool) -> None:
    global active
    active = value

def set_filter(filter:int) -> None:
    global allowed_message_types

    match filter:
        case FilterTypes.NONE:
            allowed_message_types = []

def set_name(value:str) -> None:
    global name
    name = value

def set_separator(value:str) -> None:
    global name_separator
    name_separator = value

def set_ongoing_postfix(value:str) -> None:
    global ongoing_postfix
    ongoing_postfix = value

def log(message:str, type:int, ongoing:bool=False) -> None:
    if not active: return
    if allowed_message_types and not type in allowed_message_types: return

    print(f'{prefixes[type]} {(name + name_separator) if name else ""}{message}{ongoing_postfix if ongoing else ""}')