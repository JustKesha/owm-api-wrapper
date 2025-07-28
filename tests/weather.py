from .logger import log, MessageTypes
import weather

async def test_weather(lat:float, lon:float, expected_output) -> bool:
    log(f'Requesting data from the weather module', MessageTypes.REQUEST)
    log(f'{lat}, {lon}', MessageTypes.INPUT)

    try:
        data:weather.Weather = await weather.get_weather(lat=lat, lon=lon)
    except Exception as error:
        log(f'Something went wrong: {error}', MessageTypes.FAIL)
        return False

    output = data.time.offset

    log(expected_output, MessageTypes.EXPECTED_OUTPUT)
    log(output, MessageTypes.OUTPUT)

    if output != expected_output:
        log(f'Output from weather module didnt match the expected output ("{output}" not equal "{expected_output}")', MessageTypes.FAIL)
        return False

    log('Weather test passed', MessageTypes.PASS)
    return True