import discord
from geocode import Location
from weather import Weather

# TODO Put all messages into english.json
# TODO Add a module to get translated messages

SPEED_WIND_INGORE_MS = 1.0
SPEED_GUSTS_IGNORE_MARGIN_MS = 2.5

TEMP_FEELS_IGNORE_MARGIN_C = 1.0
TEMP_RANGE_IGNORE_MARGIN_C = 1.5

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

def get_weather_embed(location:Location, report:Weather, allow_simplification:bool=True) -> discord.Embed:
    # NOTE When allow_simplification set to True some data (which was found irrelevant using the relevant consts) will be hidden

    # STATIC ELEMENTS

    embed = discord.Embed(
        title = location.get_address_str(),
        url = location.get_google_maps_url(),
        color = report.color.dex,
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

    temperature_field_elements = [
        f'Current {report.temperature.actual.c.get_str()}',
    ]

    temp_current_c = report.temperature.actual.c.get_value()
    temp_feels_c = report.temperature.feels_like.c.get_value()

    if abs(temp_current_c - temp_feels_c) >= TEMP_FEELS_IGNORE_MARGIN_C or not allow_simplification:
        temperature_field_elements.append(f'Feels like {report.temperature.feels_like.c.get_str(accuracy=0)}')
    
    temp_min_c = report.temperature.min.c.get_value()
    temp_max_c = report.temperature.max.c.get_value()

    if((abs(temp_current_c - temp_min_c) >= TEMP_RANGE_IGNORE_MARGIN_C or
        abs(temp_current_c - temp_max_c) >= TEMP_RANGE_IGNORE_MARGIN_C) or not allow_simplification):
        temperature_field_elements.append(f'Ranging from {report.temperature.min.c.get_str()} to {report.temperature.max.c.get_str()}')
    
    embed.add_field(
        name = 'Temperature',
        value = ',\n'.join(temperature_field_elements) + '.',
        inline = True,
        )
    
    # WHITE SPACE

    embed.add_field(name=' ', value=' ', inline=True)
    
    # WIND

    wind_field_elements = []

    wind_speed_ms = report.wind.speed.ms.get_value()

    if wind_speed_ms <= SPEED_WIND_INGORE_MS and allow_simplification:

        wind_field_elements = [
            'None'
            ]

    else:

        wind_field_elements = [
            f'Speed {report.wind.speed.ms.get_str()}',
            ]
        
        wind_gusts_ms = report.wind.gusts.ms.get_value()

        if wind_gusts_ms - wind_speed_ms >= SPEED_GUSTS_IGNORE_MARGIN_MS or not allow_simplification:
            wind_field_elements.append(f'Gusts up to {report.wind.gusts.ms.get_str()}')
        
        wind_field_elements.append(f'Coming from {report.wind.cardinal_point.long}',)

    embed.add_field(
        name = 'Wind',
        value = ',\n'.join(wind_field_elements) + '.',
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

# NOTE Not used atm
def create_code_block(code:str, format:str='', cut:str='...', character_limit:int=2000) -> str:
    header = f'```{format}' + ('\n' if len(format) > 0 else '')
    footer = f'```'

    character_limit -= len(''.join([header, footer]))

    if len(code) > character_limit:
        code = code[:character_limit - len(cut)] + cut
    
    return header + code + footer
