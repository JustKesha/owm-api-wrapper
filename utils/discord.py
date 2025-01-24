import discord

from geocode import Location
from weather import Weather
from .general import wrap_text_block

# TODO Put all messages into english.json
# TODO Move back to bot package (both will have to use the same english.json)

SPEED_WIND_INGORE_MS = 1.0
SPEED_GUSTS_IGNORE_MARGIN_MS = 2.5
SPEED_GUSTS_IGNORE_DIRECTION = 5.0

TEMP_FEELS_IGNORE_MARGIN_C = 2.5
TEMP_RANGE_IGNORE_MARGIN_C = 1.5

def get_error_message(
        error='Looks like something went wrong.',
        solution='Maybe try again later?',
        reaction='Whoops'
    ) -> str:
    if error:
        error += '\n'

    return f'{reaction},\n\n{error}{solution}'

def get_weather_embed(
        location:Location,
        report:Weather,
        system:int=None,
        time_format:str=None,
        time_format_long:str=None,
        allow_simplification:bool=True,
        thumbnail_attachment:str='',
        join:str=', ',
        end:str='.',
    ) -> discord.Embed:
    '''
    NOTE When allow_simplification set to True some data will be hidden if found neglectable
    '''

    if system is None:
        system = report.system

    if time_format is None:
        time_format = report.time_format

    if time_format_long is None:
        time_format_long = report.time_format_long

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

    footer_text = location.get_address_str(full=True)

    footer_time = report.time.get_str(
        seconds=report.time.get_current(),
        format=time_format_long
    )
    footer_text += f' - {footer_time}'

    embed.set_footer(text=footer_text)

    # THUMBNAIL

    thumbnail_url = report.default_icon_url

    if thumbnail_attachment:
        thumbnail_url = 'attachment://' + thumbnail_attachment

    embed.set_thumbnail(url=thumbnail_url)
    
    # TEMEPERATURE

    temp_current = report.temperature.actual.get_str(
        system=system,
        accuracy=values_accuracy, )

    temp_elements = [
        f'Current {temp_current}',
    ]

    temp_current_c = report.temperature.actual.c.get_value()
    temp_feels_c = report.temperature.feels_like.c.get_value()

    if abs(temp_current_c - temp_feels_c) >= TEMP_FEELS_IGNORE_MARGIN_C or not allow_simplification:

        temp_feels = report.temperature.feels_like.get_str(
            system=system,
            accuracy=values_accuracy, )

        temp_elements.append(f'Feels like {temp_feels}')
    
    temp_min_c = report.temperature.min.c.get_value()
    temp_max_c = report.temperature.max.c.get_value()

    show_min_temp = abs(temp_current_c - temp_min_c) >= TEMP_RANGE_IGNORE_MARGIN_C
    show_max_temp = abs(temp_current_c - temp_max_c) >= TEMP_RANGE_IGNORE_MARGIN_C

    temp_min = report.temperature.min.get_str(
        system=system,
        accuracy=values_accuracy, )
    
    temp_max = report.temperature.max.get_str(
        system=system,
        accuracy=values_accuracy, )

    if show_min_temp and show_max_temp or not allow_simplification:
        temp_elements.append(f'Ranging from {temp_min} to {temp_max}')

    elif show_min_temp:
        temp_elements.append(f'Goes down to {temp_min}')
    
    elif show_max_temp:
        temp_elements.append(f'Goes up to {temp_max}')

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

        sunrise_stamp = report.time.get_str(
            seconds=report.time.sunrise,
            format=time_format, )
        
        details_elements.append(f'sunrise {sunrise_stamp}')
        showing_sunrise = True
    
    if( not report.time.is_past_sunset
        and not showing_sunrise
        or not allow_simplification ):

        sunset_stamp = report.time.get_str(
            seconds=report.time.sunset,
            format=time_format, )

        details_elements.append(f'sunset {sunset_stamp}')

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