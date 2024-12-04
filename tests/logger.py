class MessageTypes():
    REQUEST = 0
    INPUT = 1
    OUTPUT = 2
    EXPECTED_OUTPUT = 3
    FAIL = 4
    PASS = 5

class MessageFilters():
    NONE = 0
    ONLY_RESULTS = 1
    ONLY_ERRORS = 2

active = True
allowed_message_types = []

def set_active(value:bool=True) -> None:
    global active

    active = value

def set_filter(message_filter:int) -> None:
    global allowed_message_types

    match message_filter:

        case MessageFilters.NONE:
            allowed_message_types = []

        case MessageFilters.ONLY_RESULTS:
            allowed_message_types = [
                MessageTypes.FAIL,
                MessageTypes.PASS,
            ]

        case MessageFilters.ONLY_ERRORS:
            allowed_message_types = [
                MessageTypes.FAIL,
            ]

def log(message:str, type:int) -> None:
    if not active: return
    if allowed_message_types and not type in allowed_message_types: return

    prefix = ''
    postfix = ''

    match type:

        case MessageTypes.REQUEST:
            prefix = '\n  -- '

        case MessageTypes.INPUT:
            prefix = '  -> "'
            postfix = '"'

        case MessageTypes.EXPECTED_OUTPUT:
            prefix = '   ? "'
            postfix = '"'

        case MessageTypes.OUTPUT:
            prefix = '  <- "'
            postfix = '"'

        case MessageTypes.FAIL:
            prefix = 'FAIL '
            
        case MessageTypes.PASS:
            prefix = 'PASS '
    
    print(prefix + str(message) + postfix)