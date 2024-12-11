import utils
from utils import convert
from . import globals
from . import color

# TODO Should probably save all the accuracy values set below as consts

class MeasurementSystems():
    METRIC = 0
    IMPERIAL = 1

    DEFAULT = METRIC
    VALUES = [METRIC, IMPERIAL]

# NOTE Worth mentioning that this is strictly a numeric/float value and should probably be renamed to represent that better
class Value():
    def __init__(self, value, unit:str, accuracy:int=2, separator:str=' ') -> None:
        self.set_value(value)
        self.set_unit(unit)
        self.set_accuracy(accuracy)
        self.set_separator(separator)
    
    def set_value(self, value):
        self.value = value

    def set_unit(self, unit:str):
        # TODO Short / long versions ?
        self.unit = unit

    def set_accuracy(self, accuracy:int):
        self.output_accuracy = accuracy

    def set_separator(self, separator:str):
        self.separator = separator

    def get_value(self, accuracy:int=None, remove_trailing_zeros:bool=True) -> float:
        if accuracy is None: accuracy = self.output_accuracy

        output = round(self.value, accuracy)

        if remove_trailing_zeros:
            output = utils.remove_trailing_zeros(output)

        return output

    def get_str(self, separator:str=None, accuracy:int=None) -> str:
        if separator is None: separator = self.separator

        value = self.get_value(accuracy)
        unit = self.unit

        return separator.join([str(value), unit])

class Temperature():
    def __init__(self, k:float=None) -> None:
        self.c = Value(convert.k_to_c(k), '°C', 1)
        self.f = Value(convert.k_to_f(k), '°F', 1)
        self.k = Value(k, 'K', 0)
    
    def get_str(
            self,
            system:int=MeasurementSystems.DEFAULT,
            separator:str=None,
            accuracy:int=None,
        ):
        if not system in MeasurementSystems.VALUES:
            system = MeasurementSystems.DEFAULT
        
        match system:
            case MeasurementSystems.METRIC:
                return self.c.get_str(separator=separator, accuracy=accuracy)
            case MeasurementSystems.IMPERIAL:
                return self.f.get_str(separator=separator, accuracy=accuracy)
            
class TemperatureData():
    def __init__(
            self,
            actual:Temperature,
            min:Temperature,
            max:Temperature,
            feels_like:Temperature,
        ) -> None:

        self.actual = actual
        self.min = min
        self.max = max
        self.feels_like = feels_like

class Pressure():
    def __init__(self, mbar:float=None) -> None:
        self.hpa = Value(mbar, 'hPa', 0)
        self.mmhg = Value(convert.mbar_to_mmhg(mbar), 'mmHg', 0)
        self.mbar = Value(mbar, 'Mbar', 0)

        self.index = convert.get_pressure_index(self.mmhg.get_value())
        self.name = globals.ENGLISH['pressure'][self.index]
    
    def get_str(
            self,
            system:int=MeasurementSystems.DEFAULT,
            separator:str=None,
            accuracy:int=None
        ) -> str:

        if not system in MeasurementSystems.VALUES:
            system = MeasurementSystems.DEFAULT

        output = self.name

        output += ' '
        match system:
            case MeasurementSystems.METRIC:
                output += self.mmhg.get_str(separator=separator, accuracy=accuracy)
            case MeasurementSystems.IMPERIAL:
                output += self.mbar.get_str(separator=separator, accuracy=accuracy)

        return output

class PressureData():
    def __init__(
            self,
            sea_level:Pressure,
            ground_level:Pressure,
        ) -> None:

        self.sea_level = sea_level
        self.ground_level = ground_level

class Speed():
    def __init__(self, ms:float=0, accuracy:int=1) -> None:
        
        self.ms = ms

        self.set_accuracy(accuracy)
    
    def set_accuracy(self, accuracy:int):
        self.accuracy = accuracy # is it even used?

        self.set_ms(self.ms)

    def set_ms(self, ms:float):
        self.ms = Value(ms, 'ms', 1)
        self.kph = Value(convert.ms_to_kph(ms), 'kph', 1)
        self.mph = Value(convert.ms_to_mph(ms), 'mph', 0)
        self.knots = Value(convert.ms_to_knots(ms), 'knots', 0)
    
    def get_str(
            self,
            system:int=MeasurementSystems.DEFAULT,
            separator:str=None,
            accuracy:int=None,
        ):
        if not system in MeasurementSystems.VALUES:
            system = MeasurementSystems.DEFAULT
        
        match system:
            case MeasurementSystems.METRIC:
                return self.ms.get_str(separator=separator, accuracy=accuracy)
            case MeasurementSystems.IMPERIAL:
                return self.mph.get_str(separator=separator, accuracy=accuracy)

class CardinalPoint():
    def __init__(self, degree:float) -> None:

        cardinal_point = globals.ENGLISH['cardinal_points'][convert.degree_to_cardinal_point_id(degree)]

        self.short:str = cardinal_point['short']
        self.long:str = cardinal_point['long']

class Wind():
    def __init__(self, speed:Speed, gusts:Speed, degree:float) -> None:
        self.speed = speed
        self.gusts = gusts

        self.beaufort_scale = utils.clamp(convert.knots_to_beaufort_scale_index(speed.knots.value), 0, 17)
        self.name:str = globals.ENGLISH['wind'][self.beaufort_scale]

        self.degree = Value(degree, '°', 0, '')
        self.cardinal_point = CardinalPoint(degree)

class Timezone():
    def __init__(self, offset_ms:int=0) -> None:
        self.set_offset(offset_ms)
    
    # TODO Should add such setters to the rest of the classes
    # Or predent like it was never here, bc im not gonna use them anyway
    def set_offset(self, ms:int=0) -> None:
        self.offset = ms

class Visibility():
    def __init__(self, m:float) -> None:
        self.m = Value(m, 'm', 0)
        self.km = Value(m/1000, 'km', 1)
        self.mi = Value(convert.m_to_mi(m), 'miles', 2)

        self.index = convert.get_visibility_index(self.m.get_value())
        self.name:str = globals.ENGLISH['visibility'][self.index]
    
    def get_str(
            self,
            system:int=MeasurementSystems.DEFAULT,
            force_compelte:bool=False,
            separator:str=None,
            accuracy:int=None
    ) -> str:
        # NOTE force_compelte true makes it so the numeric value is always to be added, even if the name string is self descriptive
        
        if not system in MeasurementSystems.VALUES:
            system = MeasurementSystems.DEFAULT

        output = self.name
    
        if self.index == 5 and not force_compelte:
            return output

        output += ' '
        match system:
            case MeasurementSystems.METRIC:
                if self.m.get_value() > 1000:
                    output += self.km.get_str()
                else:
                    output += self.m.get_str()
            case MeasurementSystems.IMPERIAL:
                output += self.mi.get_str(separator=separator, accuracy=accuracy)

        return output

class Humidity():
    def __init__(self, humidity:int) -> None:
        self.percentage = Value(humidity, '%', 0, '')
        
        self.index = convert.get_humidity_index(humidity)
        self.name:str = globals.ENGLISH['humidity'][self.index]
    
    def get_str(self, separator:str=None, accuracy:int=None) -> str:
        output = self.name

        if not self.index in [0, 4]:
            output += f' {self.percentage.get_str(separator=separator, accuracy=accuracy)}'
        
        return output

class Cloudiness():
    def __init__(self, cloudiness:int) -> None:
        self.percentage = Value(cloudiness, '%', 0, '')
        
        self.index = convert.get_cloudiness_index(cloudiness)
        self.name:str = globals.ENGLISH['cloudiness'][self.index]
    
    def get_str(self, separator:str=None, accuracy:int=None) -> str:
        output = self.name

        if not self.index in [0, 4]:
            output += f' {self.percentage.get_str(separator=separator, accuracy=accuracy)}'
        
        return output

class Color():
    def __init__(self, hex:str) -> None:
        self.hex = hex
        self.dex = convert.hex_to_dex(hex)

class Weather():
    def __init__(
            self,

            title:str,
            description:str,
            weather_code:int,
            default_icon_url:str,

            temperature:TemperatureData,
            wind:Wind,

            humidity:Humidity,
            pressure:PressureData,
            clouds:Cloudiness,
            visibility:Visibility,

            sunrise:int,
            sunset:int,
            timezone:Timezone,
        ) -> None:

        self.title = title
        self.description = description
        self.weather_code = weather_code
        self.default_icon_url = default_icon_url

        self.temperature = temperature
        self.wind = wind

        self.humidity = humidity
        self.pressure = pressure
        self.clouds = clouds
        self.visibility = visibility

        self.sunrise = sunrise
        self.sunset = sunset
        self.timezone = timezone

        self.color = Color(color.get_weather_hex(
            weather_code = self.weather_code,
            temp_c = self.temperature.feels_like.c.get_value(),
        ))

def format_data(raw_data:dict) -> Weather:
    # Not partly raw, but medium rare
    return Weather(
        title = raw_data['weather'][0]['main'],
        description = raw_data['weather'][0]['description'],

        temperature = TemperatureData(
            actual = Temperature(raw_data['main']['temp']),
            min = Temperature(raw_data['main']['temp_min']),
            max = Temperature(raw_data['main']['temp_max']),
            feels_like = Temperature(raw_data['main']['feels_like']),
        ),
        wind = Wind(
            speed = Speed(raw_data['wind']['speed']),
            gusts = Speed(raw_data['wind']['gust'] if 'gust' in raw_data['wind'] else raw_data['wind']['speed']),
            degree = raw_data['wind']['deg'],
        ),
        weather_code = raw_data['weather'][0]['id'],
        default_icon_url = f'https://openweathermap.org/img/wn/{raw_data["weather"][0]["icon"]}@2x.png',

        humidity = Humidity(raw_data['main']['humidity']),
        pressure = PressureData(
            sea_level = Pressure(raw_data['main']['sea_level']),
            ground_level = Pressure(raw_data['main']['grnd_level']),
        ),
        clouds = Cloudiness(raw_data['clouds']['all']),
        visibility = Visibility(raw_data['visibility']),

        sunrise = raw_data['sys']['sunrise'],
        sunset = raw_data['sys']['sunset'],
        timezone = Timezone(raw_data['timezone']),
    )