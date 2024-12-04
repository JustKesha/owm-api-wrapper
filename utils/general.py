def clamp(num:int, num_min:int, num_max:int) -> int:
    return max(min(num, num_max), num_min)