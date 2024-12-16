from datetime import datetime

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

def upcase_first_char(s:str) -> str:
    return s[0].upper() + s[1:]

def is_it_past_time(
        some_time:float,
        timezone_offset:float=0,
        utc_time:float=None,
        ) -> bool:
    if utc_time is None:
        utc_time = datetime.utcnow().timestamp()
    
    return utc_time + timezone_offset > some_time
