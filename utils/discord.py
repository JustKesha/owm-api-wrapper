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
    embed.set_author(name="Viewing current weather in,")

    embed.add_field(
        name = 'Temperature',
        value =
            ',\n'.join([
                f'Current {report.temperature.actual.c.get_str()}',
                f'Feels like {report.temperature.feels_like.c.get_str()}',
                f'Ranging {report.temperature.min.c.get_str()} to {report.temperature.max.c.get_str()}',
                ]) + '.',
        inline = True,
        )
    
    # Adds some more space in between inline feields
    embed.add_field(name=' ', value=' ', inline=True)
    
    embed.add_field(
        name = 'Wind',
        value =
            ',\n'.join([
                f'Speed {report.wind.speed.ms.get_str()}',
                f'Gusts up to {report.wind.gusts.ms.get_str()}',
                f'Coming from {report.wind.cardinal_point.long}',
                # f'Comin from {report.wind.cardinal_point.long} ({report.wind.cardinal_point.short}) {report.wind.degree.get_str()}',
                ]) + '.',
        inline = True,
        )
    
    # DETAILS FEILD

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Continue here...
    # TODO Add .get_str to all the following elements (like was done with humidity below)

    clouds_str = f'lots of clouds {report.clouds.get_str()}'
    pressure_str = f'low pressure {report.pressure.ground_level.mbar.get_str()}'
    visibility_str = f'great visibility {report.visibility.m.get_str()}'

    embed.add_field(
        name = 'Details',
        value = ', '.join([report.humidity.get_str().capitalize(), clouds_str, '\n' + pressure_str.capitalize(), visibility_str]) + '.',
        inline = False,
        )

    embed.set_thumbnail(url=report.default_icon_url)
    embed.set_footer(text=location.get_address_str(full=True))

    return embed

def create_code_block(code:str, format:str='', cut:str='...', character_limit:int=2000) -> str:
    header = f'```{format}' + ('\n' if len(format) > 0 else '')
    footer = f'```'

    character_limit -= len(''.join([header, footer]))

    if len(code) > character_limit:
        code = code[:character_limit - len(cut)] + cut

    return header + code + footer
