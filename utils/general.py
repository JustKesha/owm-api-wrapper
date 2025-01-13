from datetime import datetime
from typing import List

# NUMBERS

def clamp(num:int, num_min:int, num_max:int) -> int:
    return max(min(num, num_max), num_min)

def has_floating_point(value) -> bool:
    return '.' in str(value)

def remove_trailing_zeros(num:float):
    no_zeros_str = ('%f' % num).rstrip('0').rstrip('.')
    
    # Doing just float will result in .0 added to the end
    if has_floating_point(no_zeros_str):
        return float(no_zeros_str)
    
    return int(no_zeros_str)

# STRINGS

def upcase_first_char(s:str) -> str:
    return s[0].upper() + s[1:]

# ARRAYS

def wrap_text_block(
        block_elements:List[str],
        elements_in_row:int=2,
        capitalize_rows:bool=True,
        join:str=', ',
        row_end:str=',\n',
        end:str='.',
        ) -> str:
    
    result = ''
    new_row = True
    for i, el in enumerate(block_elements):

        if new_row and capitalize_rows:
            el = upcase_first_char(el)
            new_row = False
        
        result += el

        if i == len(block_elements) - 1:
            result += end
        elif (i + 1) % elements_in_row == 0:
            result += row_end
            new_row = True
        else:
            result += join
    
    return result

# TIME

def get_utc_time() -> float:
    return datetime.utcnow().timestamp()

def unix_time_to_str(seconds:float) -> str:
    # NOTE In discord, decided to use embed timestamps
    # Leaving it be for other platforms / if gonna stop using embed timestamps
    dt = datetime.fromtimestamp(seconds)
    # Doing this instead of strftime to avoid leading zeros in day & hour
    return f'{dt:%A} {dt.hour}:{dt:%M} {dt:%p}, {dt:%b} {dt.day}'

def is_it_past_time(
        some_time:float,
        timezone_offset:float=0,
        utc_time:float=None,
        ) -> bool:
    if utc_time is None:
        utc_time = get_utc_time()
    
    return utc_time + timezone_offset > some_time