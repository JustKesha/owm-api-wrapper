from . import globals

def get_hex_by_temperature(c:float) -> str:
    arr = globals.DATA['colors_by_temperature']
    max_i = len(arr) - 1

    for i in range(max_i + 1):
        if i == max_i or c <= arr[i]['max_c']:
            return arr[i]['hex']
