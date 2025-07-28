from .geocode import test_geocode
from .weather import test_weather

async def run_tests(
        geocode_ins:list=[
            'спб',
            'мск',
        ],
        geocode_outs:list=[
            'Saint Petersburg, Russia',
            'Moscow, Russia',
        ],
        
        weather_lats:list=[
            53.2001,
        ],
        weather_lons:list=[
            50.15,
        ],
        weather_outs:list=[
            14400,
        ],
    ) -> bool:

    for i in range(len(geocode_ins)):
        if not test_geocode(geocode_ins[i], geocode_outs[i]): return False
    
    for i in range(len(weather_lats)):
        if not await test_weather(weather_lats[i], weather_lons[i], weather_outs[i]): return False
    
    return True