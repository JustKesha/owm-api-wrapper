# PRESSURE

def mbar_to_mmhg(mbar:float) -> float:
    return mbar * 0.7500637554

# TEMPERATURE

def k_to_c(c:float) -> float:
    return c - 273.15

def k_to_f(c:float) -> float:
    return (c - 273.15) * 9/5 + 32

# SPEED

def ms_to_kph(ms:float) -> float:
    return ms * 3.6

def ms_to_mph(ms:float) -> float:
    return ms * 2.23694

def ms_to_knots(ms:float) -> float:
    return ms * 1.943844

# DISTANCE

def m_to_mi(m:float) -> float:
    return m * 0.000621371

# COLOR

def hex_to_dex(hex:str) -> int:
    return int(hex.replace('#', ''), 16)

# WIND

BEAUFORT_SCALE = [
    # NOTE The opening value's ceiling is non inclusive unlike the rest
    { 'max_knots': 1 },
    
    { 'max_knots': 3   },
    { 'max_knots': 6   },
    { 'max_knots': 10  },
    { 'max_knots': 16  },
    { 'max_knots': 21  },
    { 'max_knots': 27  },
    { 'max_knots': 33  },
    { 'max_knots': 40  },
    { 'max_knots': 47  },
    { 'max_knots': 55  },
    { 'max_knots': 63  },
    { 'max_knots': 72  },
    { 'max_knots': 85  },
    { 'max_knots': 89  },
    { 'max_knots': 99  },
    { 'max_knots': 106 },

    # NOTE The closing value doesnt have a ceiling
    { }
]

def knots_to_beaufort_scale_index(knots:float) -> int:
    max_i = len(BEAUFORT_SCALE) - 1

    for i in range(max_i + 1):
        # I didnt find the match construction to be possible here

        if i == max_i:
            return i
        
        ceiling = BEAUFORT_SCALE[i]['max_knots']
        
        if i == 0 and knots < ceiling:
            return i
        
        if knots <= ceiling:
            return i

# CUSTOM

def get_humidity_index(humidity:int) -> int:
    if   humidity == 0:
        return 0
    elif humidity < 30:
        return 1
    elif humidity < 65:
        return 2
    elif humidity != 100:
        return 3
    else:
        return 4

def get_cloudiness_index(cloudiness:int) -> int:
    if   cloudiness == 0:
        return 0
    elif cloudiness < 35:
        return 1
    elif cloudiness < 65:
        return 2
    elif cloudiness < 100:
        return 3
    else:
        return 4

def get_visibility_index(visibility_m:int) -> int:
    if   visibility_m < 150:
        return 0
    elif visibility_m < 300:
        return 1
    
    elif visibility_m < 5000:
        return 2
    
    elif visibility_m < 8000:
        return 3
    elif visibility_m < 10000:
        return 4
    else:
        return 5

AVARAGE_PRESSURE_MMHG = 760
NORM_PRESSURE_RANGE_MMHG = 30

def get_pressure_index(pressure_mmhg:float) -> int:
    if   pressure_mmhg <= AVARAGE_PRESSURE_MMHG - NORM_PRESSURE_RANGE_MMHG / 2:
        return 0
    elif pressure_mmhg <= AVARAGE_PRESSURE_MMHG + NORM_PRESSURE_RANGE_MMHG / 2:
        return 1
    else:
        return 2

# CARDINAL POINTS

def degree_to_cardinal_point_id(degree:float) -> int:
    if   degree < 22.5:
        return 0
    elif degree < 67.5:
        return 1
    elif degree < 112.5: 
        return 2
    elif degree < 157.5: 
        return 3
    elif degree < 202.5: 
        return 4
    elif degree < 247.5: 
        return 5
    elif degree < 292.5: 
        return 6
    elif degree < 337.5: 
        return 7
    else:
        return 0