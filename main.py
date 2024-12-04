import os

import asyncio
import nest_asyncio
import dotenv

import tests
import geocode
import weather
import bot

def configurate():
    print('/ configuring project')

    dotenv.load_dotenv()

    weather.configurate(base_url=os.getenv('OPENWEATHER_BASE_URL'), key=os.getenv('OPENWEATHER_API_KEY'))
    geocode.configurate(user_agent=os.getenv('USER_AGENT'))
    bot.configurate(api_key=os.getenv('DISCORD_API_KEY'), test_guild_ids=[os.getenv('DISCORD_TEST_GUILD_ID')])

async def run_tests(logger_filter:int=tests.logger.MessageFilters.ONLY_RESULTS) -> bool:
    print('/ running basic module tests')

    tests.logger.set_filter(logger_filter)
    
    return await tests.run_tests()

def run_bot():
    print('/ runnig bot')
    
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

# This all is just for the sole purpose of using the silly tests i wrote
# And it seems like bit too much, I might just wanna remove em bc +2 dependencies
if __name__ ==  '__main__':
    nest_asyncio.apply()
    loop = asyncio.get_event_loop()
    loop.run_until_complete( main() )
    