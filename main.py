import os
import asyncio
import nest_asyncio
import dotenv
import tests
import geocode
import weather
from tests.logger import MessageFilters

def init():
    dotenv.load_dotenv()
    weather.configurate(
        base_url = os.getenv('OPENWEATHER_BASE_URL'),
        key = os.getenv('OPENWEATHER_API_KEY')
        )
    geocode.configurate(user_agent = os.getenv('USER_AGENT'))

async def test(log_filter: int = MessageFilters.ONLY_RESULTS) -> bool:
    tests.logger.set_filter(log_filter)
    return await tests.run_tests()

async def main(
        run_tests: bool = False,
        logger_mode: MessageFilters = MessageFilters.ONLY_RESULTS
        ):
    init()

    if run_tests and not await test(logger_mode):
        return print("ERR Some of the tests failed")
    
    # EXAMPLE USAGE
    where = input("Enter location name: ")
    place = geocode.get_location(where)
    weath = await weather.get_weather(place.lat, place.lon)
    print(weath)

if __name__ ==  '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete( main(run_tests = False) )
