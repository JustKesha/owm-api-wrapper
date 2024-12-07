def clamp(num:int, num_min:int, num_max:int) -> int:
    return max(min(num, num_max), num_min)

def has_floating_point(value) -> bool:
    return '.' in str(value)

def remove_trailing_zeros(num:float):
    # This might have some issues, look into https://stackoverflow.com/a/2440786/16652135
    no_zeros_str = ('%f' % num).rstrip('0').rstrip('.')
    
    # Doing just float will result in .0 added back to the end of ints
    if has_floating_point(no_zeros_str):
        return float(no_zeros_str)
    else:
        return int(no_zeros_str)