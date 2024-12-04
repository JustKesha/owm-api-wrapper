from .logger import log, MessageTypes
import geocode
import weather

def test_geocode(input:str, expected_output) -> bool:
    log(f'Requesting data from the geocode module', MessageTypes.REQUEST)
    log(input, MessageTypes.INPUT)

    try:
        location:geocode.Location = geocode.get_location(input)
    except Exception as error:
        log(f'Something went wrong: {error}', MessageTypes.FAIL)
        return False
    
    output = location.get_address_str(full=True)

    log(expected_output, MessageTypes.EXPECTED_OUTPUT)
    log(output, MessageTypes.OUTPUT)

    if output != expected_output:
        log(f'Output from geocode module didnt match the expected output ("{output}" not equal "{expected_output}")', MessageTypes.FAIL)
        return False
    
    log('Geocode test passed', MessageTypes.PASS)
    return True

async def test_weather(lat:float, lon:float, expected_output) -> bool:
    log(f'Requesting data from the weather module', MessageTypes.REQUEST)
    log(f'{lat}, {lon}', MessageTypes.INPUT)

    try:
        data:weather.Weather = await weather.get_weather(lat=lat, lon=lon)
    except Exception as error:
        log(f'Something went wrong: {error}', MessageTypes.FAIL)
        return False

    output = data.timezone.offset

    log(expected_output, MessageTypes.EXPECTED_OUTPUT)
    log(output, MessageTypes.OUTPUT)

    if output != expected_output:
        log(f'Output from weather module didnt match the expected output ("{output}" not equal "{expected_output}")', MessageTypes.FAIL)
        return False

    log('Weather test passed', MessageTypes.PASS)
    return True

async def run_tests(
        geocode_ins:list=[
            'спб',
            'мск',
        ],
        geocode_outs:list=[
            'Saint Petersburg, Saint Petersburg, Russia',
            'Moscow, Moscow, Russia',
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