import os

import asyncio
import nest_asyncio
import dotenv

import tests
import geocode
import weather
import bot
from tests.logger import MessageFilters

def configurate():
    print('/ configuring project')

    dotenv.load_dotenv()

    weather.configurate(
        base_url=os.getenv('OPENWEATHER_BASE_URL'),
        key=os.getenv('OPENWEATHER_API_KEY') )
    
    geocode.configurate(user_agent=os.getenv('USER_AGENT'))

    test_guild = os.getenv('DISCORD_TEST_GUILD_ID')

    bot.configurate(
        api_key=os.getenv('DISCORD_API_KEY'),
        test_guild_ids=[test_guild] if test_guild else None )

async def run_tests(log_filter:int=MessageFilters.ONLY_RESULTS) -> bool:
    print('/ running basic module tests')

    tests.logger.set_filter(log_filter)
    
    return await tests.run_tests()

def run_bot(log_filter:list=bot.log.Filters.NONE):
    print('/ starting the bot')

    bot.log.set_filter(log_filter)
    
    try:
        bot.start()
    except Exception as e:
        raise e

async def main(include_tests:bool=False):
    print('/ starting')

    configurate()

    if include_tests and not await run_tests():
        return

    try:
        run_bot()
    except Exception as e:
        print('! something went wrong:', e)
        return

# Doing this to be able to run custom tests
# Might consider removing due to 2 dependencies
if __name__ ==  '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete( main() )
    