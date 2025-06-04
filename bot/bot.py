import discord # py-cord
from discord.ext import commands

from .log import log, MessageTypes
from utils import discord as discord_utils
from geocode import get_location, Location
from weather import get_weather, Weather, MeasurementSystems, TimeFormats

configurated = False
bot:discord.Bot
key:str
test_guilds:list

def configurate(api_key:str, test_guild_ids:list=None):
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

    # LISTENERS
    @bot.listen()
    async def on_interaction(interaction:discord.Interaction):
        match interaction.type:
            case discord.InteractionType.application_command:
                author:discord.User = interaction.user

                log(f'"{author.global_name}" used some interaction', MessageTypes.INTR)
            case _:
                log('unknown interaction', MessageTypes.WARN)

    # APPLICATION COMMANDS

    @bot.slash_command(
        name='weather',
        description='Look up fresh weather anywhere in the world!',
        guild_ids=test_guilds,
    )
    @commands.cooldown(1, 5)
    async def _weather(
        ctx:discord.ApplicationContext,
        search:discord.Option(
            str,
            required=True,
            description='Enter in any city, village or town name',
        ),
        units:discord.Option(
            int,
            required=False,
            description='If not specified, will be selected according to location',
            choices=[
                discord.OptionChoice(
                    name='Metric',
                    value=MeasurementSystems.METRIC,
                ),
                discord.OptionChoice(
                    name='Imperial',
                    value=MeasurementSystems.IMPERIAL,
                ),
            ],
        )=None,
    ):
        await ctx.response.defer()

        location:Location = get_location(search)
        
        if location == None:
            return await ctx.send_followup(discord_utils.get_error_message(
                error='Couldnt pinpoint the location.',
                solution='Maybe try reformulating your query or swapping parts of your query?',
            ))

        try:
            report:Weather = await get_weather(lat=location.lat, lon=location.lon)
        except Exception as e:
            log(e, MessageTypes.WARN)
            return await ctx.send_followup(discord_utils.get_error_message(
                error='Couldnt load the weather report.',
                solution='Maybe try again later?',
            ))

        files = []
        thumbnail_attachment = ''
        icon_bytes_io = report.get_icon()

        if icon_bytes_io:
            thumbnail_attachment = 'icon.png'
            files.append(discord.File(icon_bytes_io, thumbnail_attachment))

        await ctx.send_followup(
            files=files,
            embed=discord_utils.get_weather_embed(
                location=location,
                report=report,
                system=units,
                thumbnail_attachment=thumbnail_attachment,
            ),
        )
    
    @bot.event
    async def on_application_command_error(
        ctx: discord.ApplicationContext,
        error: Exception ):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(error, ephemeral=True)

def start():
    if not configurated:
        raise Exception('Trying to start a bot before it was configurated. Make sure to first run discord.bot.configurate(...).')

    init()

    log('starting', MessageTypes.PROC, ongoing=True)
    
    try:
        bot.run(key)
    except Exception as e:
        raise e
