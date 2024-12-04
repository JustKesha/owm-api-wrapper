import discord # py-cord

from .log import log, MessageTypes
from utils import discord as discord_utils
from geocode import get_location, Location
from weather import get_weather, Weather

configurated = False
bot:discord.Bot
key:str
test_guilds:list

def configurate(api_key:str, test_guild_ids:list=[]):
    global key, test_guilds, configurated

    key = api_key
    test_guilds = test_guild_ids
    
    configurated = True

def init():
    global bot

    log('initialising', MessageTypes.PROC, ongoing=True)

    intents = discord.Intents.default()
    intents.message_content = True

    bot = discord.Bot(intents=intents)

    # ONE CALL ONLY
    @bot.listen(once=True)
    async def on_ready():
        log('running', MessageTypes.PROC)

    # EVENTS
    @bot.event
    async def on_message(message:discord.Message):
        if message.author == bot.user: return

        log(f'"{message.author.global_name}" says "{message.content}"', MessageTypes.INFO)

    # LISTENERS
    @bot.listen()
    async def on_interaction(interaction:discord.Interaction):
        match interaction.type:
            case discord.InteractionType.application_command:
                author:discord.User = interaction.user

                # TODO Add slash command name to the print
                log(f'"{author.global_name}" used some interaction', MessageTypes.INTR)
            case _:
                log('unknown interaction', MessageTypes.WARN)

    # APPLICATION COMMANDS
    # TODO Separate into files, look into py-cord cogs
    @bot.slash_command(
        name='weather',
        description='Request fresh weather data from the API.',
        guild_ids=test_guilds,
    )
    async def _weather(ctx:discord.ApplicationContext, search:str):
        await ctx.response.defer(ephemeral=True)

        location:Location = get_location(search)
        
        if location == None:
            return await discord_utils.respond_with_error(
                ctx,
                error='Couldnt pinpoint the location.',
                solution='Maybe try reformulating your query or swapping parts of your query?',
                )

        try:
            report:Weather = await get_weather(lat=location.lat, lon=location.lon, test=True)
        except Exception as e:
            print(e)
            return await discord_utils.respond_with_error(
                ctx,
                error='Couldnt load the weather report.',
                solution='Maybe try again later?',
                )

        await ctx.send_followup(embed=discord_utils.get_weather_embed(location=location, report=report))

    @bot.slash_command(
        name='find',
        description='Gets location data from Nominatim - OpenStreetMap using GeoPy.',
        guild_ids=test_guilds,
    )
    async def _find(ctx:discord.ApplicationContext, search:str):
        await ctx.response.defer(ephemeral=True)

        location:Location = get_location(search)
        
        if location == None:
            return await discord_utils.respond_with_error(
                ctx,
                error='Couldnt find the location.',
                solution='Maybe try reformulating your query or swapping parts of your query?',
                )

        await ctx.send_followup(location.get_str())

def start():
    if not configurated:
        raise Exception('Trying to start a bot before it was configurated. Make sure to first run discord.bot.configurate(...).')

    init()

    log('starting', MessageTypes.PROC, ongoing=True)
    
    try:
        bot.run(key)
    except Exception as e:
        raise e
