import discord
from geocode import Location
from weather import Weather, MeasurementSystems

# TODO Put all messages into english.json
# TODO Move back to bot package (both will have to use the same english.json)

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

def get_weather_embed(
        location:Location,
        report:Weather,
        system:int=MeasurementSystems.METRIC,
        allow_simplification:bool=True,
    ) -> discord.Embed:
    # NOTE When allow_simplification set to True some data (which was found irrelevant using the relevant consts) will be hidden

    # STATIC ELEMENTS

    description_elements = [
        report.title.capitalize(),
    ]

    if report.title != report.description:
        description_elements.append(report.description)

    description_elements.append(report.wind.name)

    embed = discord.Embed(
        title = location.get_address_str(),
        url = location.get_google_maps_url(),
        color = report.color.dex,
        description = ', '.join(description_elements) + '.\n',
    )
    embed.set_thumbnail(url=report.default_icon_url)
    embed.set_author(name='Viewing current weather in,')
    embed.set_footer(text=location.get_address_str(full=True))

    # TEMEPERATURE

    temp_current = report.temperature.actual.get_str(system=system)

    temperature_field_elements = [
        f'Current {temp_current}',
    ]

    temp_current_c = report.temperature.actual.c.get_value()
    temp_feels_c = report.temperature.feels_like.c.get_value()

    if abs(temp_current_c - temp_feels_c) >= TEMP_FEELS_IGNORE_MARGIN_C or not allow_simplification:

        temp_feels = report.temperature.feels_like.get_str(
            system=system,
            accuracy=0
        )

        temperature_field_elements.append(f'Feels like {temp_feels}')
    
    temp_min_c = report.temperature.min.c.get_value()
    temp_max_c = report.temperature.max.c.get_value()

    if((abs(temp_current_c - temp_min_c) >= TEMP_RANGE_IGNORE_MARGIN_C or
        abs(temp_current_c - temp_max_c) >= TEMP_RANGE_IGNORE_MARGIN_C) or not allow_simplification):

        temp_min = report.temperature.min.get_str(system=system)
        temp_max = report.temperature.max.get_str(system=system)

        temperature_field_elements.append(f'Ranging from {temp_min} to {temp_max}')
    
    embed.add_field(
        name = 'Temperature',
        value = ',\n'.join(temperature_field_elements) + '.',
        inline = True,
    )
    
    # WHITE SPACE

    embed.add_field(name=' ', value=' ', inline=True)
    
    # WIND

    wind_speed_ms = report.wind.speed.ms.get_value()

    if wind_speed_ms > SPEED_WIND_INGORE_MS or not allow_simplification:
        wind_field_elements = [
            f'Speed {report.wind.speed.get_str(system=system)}',
        ]
        
        wind_gusts_ms = report.wind.gusts.ms.get_value()

        if wind_gusts_ms - wind_speed_ms >= SPEED_GUSTS_IGNORE_MARGIN_MS or not allow_simplification:
            wind_field_elements.append(f'Gusts up to {report.wind.gusts.get_str(system=system)}')
        
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
            '\n' + report.pressure.sea_level.get_str(system=system).capitalize(),
            report.visibility.get_str(system=system)]) + '.',
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
