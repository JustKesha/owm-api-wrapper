from enum import Enum
from datetime import datetime

import discord

from geocode import Location
from weather import Weather, MeasurementSystems
from .general import wrap_text_block, unix_time_to_str

# TODO Put all messages into english.json
# TODO Move back to bot package (both will have to use the same english.json)

SPEED_WIND_INGORE_MS = 1.0
SPEED_GUSTS_IGNORE_MARGIN_MS = 2.5
SPEED_GUSTS_IGNORE_DIRECTION = 5.0

TEMP_FEELS_IGNORE_MARGIN_C = 2.5
TEMP_RANGE_IGNORE_MARGIN_C = 1.5

class TimestampFormats(Enum):
    DATE = 'd'
    DATE_LONG = 'D'
    TIME = 't'
    TIME_LONG = 'T'
    DATE_AND_TIME = 'f'
    DATE_AND_TIME_LONG = 'F'
    RELATIVE = 'R'

# TODO Replace with get error str
async def respond_with_error(
        ctx:discord.ApplicationContext,
        error='Looks like something went wrong.',
        solution='Maybe try again later?',
        reaction='Whoops',
        ephemeral=True
    ):
    # TODO Add a return value type hint

    if error:
        error += '\n'

    message = f'{reaction},\n\n{error}{solution}'

    return await ctx.respond(message, ephemeral=ephemeral)

def get_timestamp(time:int, format:TimestampFormats=TimestampFormats.DATE_AND_TIME_LONG) -> str:
    return f'<t:{time}:{format.value}>'

def get_weather_embed(
        location:Location,
        report:Weather,
        system:int=MeasurementSystems.METRIC,
        allow_simplification:bool=True,
        thumbnail_attachment:str='',
        join:str=', ',
        end:str='.',
        # Discord's timestamps can be pretty confusing so might move on from them
        timestamp_format:TimestampFormats=TimestampFormats.TIME,
    ) -> discord.Embed:
    '''
    NOTE When allow_simplification set to True some data will be hidden if found neglectable
    '''

    values_accuracy = 0 if allow_simplification else None

    # GENERAL

    description = join.join([
        (report.description or report.title).capitalize(),
        report.wind.name,
    ]) + end

    embed = discord.Embed(
        title = location.get_address_str(),
        url = location.get_google_maps_url(),
        color = report.color.dex,
        description = description,
    )
    embed.set_author(name='Viewing current weather in,')
    embed.set_footer(text=location.get_address_str(full=True))
    embed.timestamp = datetime.fromtimestamp(report.time.get_current())

    # THUMBNAIL

    thumbnail_url = report.default_icon_url

    if thumbnail_attachment:
        thumbnail_url = 'attachment://' + thumbnail_attachment

    embed.set_thumbnail(url=thumbnail_url)

    # TEMEPERATURE

    temp_current = report.temperature.actual.get_str(
        system=system,
        accuracy=values_accuracy,
        )

    temp_elements = [
        f'Current {temp_current}',
    ]

    temp_current_c = report.temperature.actual.c.get_value()
    temp_feels_c = report.temperature.feels_like.c.get_value()

    if abs(temp_current_c - temp_feels_c) >= TEMP_FEELS_IGNORE_MARGIN_C or not allow_simplification:

        temp_feels = report.temperature.feels_like.get_str(
            system=system,
            accuracy=values_accuracy
        )

        temp_elements.append(f'Feels like {temp_feels}')
    
    temp_min_c = report.temperature.min.c.get_value()
    temp_max_c = report.temperature.max.c.get_value()

    if((abs(temp_current_c - temp_min_c) >= TEMP_RANGE_IGNORE_MARGIN_C or
        abs(temp_current_c - temp_max_c) >= TEMP_RANGE_IGNORE_MARGIN_C) or
        not allow_simplification):

        temp_min = report.temperature.min.get_str(system=system)
        temp_max = report.temperature.max.get_str(system=system)

        temp_elements.append(f'Ranging from {temp_min} to {temp_max}')

    temp_desc = wrap_text_block(
        temp_elements,

        elements_in_row=1,
        join=join,
        end=end,
    ) if len(temp_elements) > 1 else temp_current

    embed.add_field(
        name = 'Temperature',
        value = temp_desc,
        inline = True,
    )
    
    # WHITE SPACE

    embed.add_field(name=' ', value=' ', inline=True)
    
    # WIND

    wind_speed_ms = report.wind.speed.ms.get_value()

    if wind_speed_ms > SPEED_WIND_INGORE_MS or not allow_simplification:
        wind_speed = report.wind.speed.get_str(
            system=system,
            accuracy=values_accuracy,
            )

        wind_elements = [
            f'Speed {wind_speed}',
        ]
        
        wind_gusts_ms = report.wind.gusts.ms.get_value()

        if( wind_gusts_ms - wind_speed_ms >= SPEED_GUSTS_IGNORE_MARGIN_MS
            or not allow_simplification ):

            gusts_speed = report.wind.gusts.get_str(
                system=system,
                accuracy=values_accuracy, )

            gusts_str = f'Gusts up to {gusts_speed}'

            if allow_simplification:
                wind_elements = [gusts_str]

            else:
                wind_elements.append(gusts_str)
        
        if( wind_gusts_ms >= SPEED_GUSTS_IGNORE_DIRECTION
           or not allow_simplification ):
            
            direction = report.wind.cardinal_point.long

            wind_elements.append(f'Coming from {direction}',)
        
        wind_desc = wrap_text_block(
            wind_elements,

            elements_in_row=1,
            join=join,
            end=end,
        ) if len(wind_elements) > 1 else wind_speed

        embed.add_field(
            name = 'Wind',
            value = wind_desc,
            inline = True,
        )
    
    # DETAILS

    details_elements = []

    showing_sunrise = False
    if( not report.time.is_past_sunrise
        or not allow_simplification):

        sunrise_timestamp = get_timestamp(
            report.time.sunrise,
            timestamp_format )
        
        details_elements.append(f'sunrise {sunrise_timestamp}')
        showing_sunrise = True
    
    if( not report.time.is_past_sunset
        and not showing_sunrise
        or not allow_simplification ):

        sunset_timestamp = get_timestamp(
            report.time.sunset,
            timestamp_format )

        details_elements.append(f'sunset {sunset_timestamp}')

    details_elements.append(report.humidity.get_str())
    details_elements.append(report.clouds.get_str())
    details_elements.append(report.pressure.sea_level.get_str(system=system))

    # TODO Add enums
    if not allow_simplification or report.visibility.index != 5:
        details_elements.append(report.visibility.get_str(system=system))

    embed.add_field(
        name = 'Details',
        value = wrap_text_block(
            details_elements,

            elements_in_row=2,
            join=join,
            end=end,
        ),
        inline = False,
        )

    return embed