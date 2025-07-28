from .logger import log, MessageTypes
import geocode

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
