class MessageTypes():
    PROC = 0
    WARN = 1
    INTR = 2
    INFO = 3

class Filters():
    NONE = []
    NO_INFO = [
        MessageTypes.PROC,
        MessageTypes.WARN,
        MessageTypes.INTR,
    ]

MESSAGE_PREFIXES = {
    MessageTypes.PROC: '/',
    MessageTypes.WARN: '!',
    MessageTypes.INTR: '-',
    MessageTypes.INFO: '?',
}

active = True
allowed_message_types = []

name = 'discord'
name_separator = ': '
ongoing_postfix = '...'

def set_active(value:bool) -> None:
    global active
    active = value

def set_filter(value:list) -> None:
    global allowed_message_types
    allowed_message_types = value

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

    print(f'{MESSAGE_PREFIXES[type]} {(name + name_separator) if name else ""}{message}{ongoing_postfix if ongoing else ""}')