import discord
from geocode import Location
from weather import Weather

# TODO Put all messages into english.json
# TODO Add a module to get translated messages

async def respond_with_error(
        ctx:discord.ApplicationContext,
        error='Looks like something went wrong.',
        solution='Maybe try again later?',
        reaction='Whoops',
        ephemeral=True
    ):

    if len(error) > 0:
        error += '\n'

    message = f'{reaction},\n\n{error}{solution}'

    return await ctx.respond(message, ephemeral=ephemeral)

def get_weather_embed(location:Location, report:Weather) -> discord.Embed:
    # STATIC ELEMENTS

    embed = discord.Embed(
        title = location.get_address_str(),
        url = location.get_google_maps_url(),
        description =
            ', '.join([
                report.title,
                report.description,
                report.wind.name
                ]) + '.\n'
    )
    embed.set_thumbnail(url=report.default_icon_url)
    embed.set_author(name="Viewing current weather in,")
    embed.set_footer(text=location.get_address_str(full=True))

    # TEMEPERATURE

    embed.add_field(
        name = 'Temperature',
        value =
            ',\n'.join([
                f'Current {report.temperature.actual.c.get_str()}',
                f'Feels like {report.temperature.feels_like.c.get_str()}',
                f'Ranging from {report.temperature.min.c.get_str()} to {report.temperature.max.c.get_str()}',
                ]) + '.',
        inline = True,
        )
    
    # WHITE SPACE

    embed.add_field(name=' ', value=' ', inline=True)
    
    # WIND

    embed.add_field(
        name = 'Wind',
        value =
            ',\n'.join([
                f'Speed {report.wind.speed.ms.get_str()}',
                f'Gusts up to {report.wind.gusts.ms.get_str()}',
                f'Coming from {report.wind.cardinal_point.long}',
                ]) + '.',
        inline = True,
        )
    
    # DETAILS

    embed.add_field(
        name = 'Details',
        value = ', '.join([
            report.humidity.get_str().capitalize(),
            report.clouds.get_str(),
            '\n' + report.pressure.sea_level.get_str(report.pressure.sea_level.OUTPUT_MODES.MMHG).capitalize(),
            report.visibility.get_str(report.visibility.OUTPUT_MODES.M_OR_KM)]) + '.',
        inline = False,
        )

    return embed

# NOTE Might not be used atm
def create_code_block(code:str, format:str='', cut:str='...', character_limit:int=2000) -> str:
    header = f'```{format}' + ('\n' if len(format) > 0 else '')
    footer = f'```'

    character_limit -= len(''.join([header, footer]))

    if len(code) > character_limit:
        code = code[:character_limit - len(cut)] + cut

    return header + code + footer
