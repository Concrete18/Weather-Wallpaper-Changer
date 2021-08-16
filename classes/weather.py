from classes.logging import Logger
import datetime as dt
import requests

class Weather(Logger):


    def __init__(self, api_key, temp_unit, zipcode=None, country='us', lat=None, lon=None):
        '''
        Requies an `api_key`.

        `zipcode` is required while country is optional unless outside of the us.

        If Zipcode is not used then `lat` and `lon` are required.
        '''
        self.api_key = api_key
        self.temp_unit = temp_unit
        self.zipcode = zipcode
        self.country = country
        self.lat = lat
        self.lon = lon


    def create_api_url(self, location_mode):
        '''
        Sets up the Weather API URL.
        '''
        base_url = 'http://api.openweathermap.org/data/2.5/weather?'
        if location_mode == 'coord':  # Sets url to use coordinates
            api_url = f'{base_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}'
        elif location_mode == 'zip':  # Sets url to use zip code
            api_url = f'{base_url}zip={self.zipcode},{self.country}&appid={self.api_key}'
        else:
            self.logger.error(f'Missing Location_Mode value in config.')
        self.logger.debug(api_url)
        return api_url


    @staticmethod
    def convert_temp(temp, unit):
        '''
        Converts given temperature from kelvin into Fahrenheit or Celsius.

        `temp` temperature to convert.

        `unit` of to conver to.
        '''
        if unit == 'f':
            return f'{round(temp*9/5-459.67, 1)}°F'
        elif unit == 'c':
            return f'{round(temp-273.15, 1)}°C'
        else:
            raise Exception('Invalid unit of temperture.')


    def check(self, location_mode):
        '''
        Checks the weather and updates the self.current_weather var with the data.
        '''
        api_url = self.create_api_url(location_mode)
        cur_temp = None
        try:
            response = requests.get(api_url)  # get method of requests module
            data = response.json()  # json method of response object that converts json format data into python dict
        except:
            self.logger.critical('No data found for entered location.')
            default_tray_info = f'{self.title}\nNo Data Found'
            self.tray.update(tooltip=default_tray_info)
            return
        if 'weather' in data:
            weather = data["weather"]  # store the value of "weather" key in variable weather
            weather_description = weather[0]["description"]
            if 'temp' in data['main']:
                cur_temp = self.convert_temp(data['main']['temp'], self.temp_unit)
            sunset_time = self.convert_utc(data["sys"]['sunset'])
            sunrise_start = self.convert_utc(data["sys"]['sunrise'])
            sunset_length, sunrise_length = 20, 20
            sunrise_end = sunrise_start + dt.timedelta(minutes=sunrise_length, seconds=-1)
            sunset_end = sunset_time + dt.timedelta(seconds=-1)
            sunset_start = sunset_end + dt.timedelta(minutes=-sunset_length) + dt.timedelta(seconds=1)
            day_start = sunrise_end + dt.timedelta(seconds=1)
            day_end = sunset_start + dt.timedelta(seconds=-1)
            return {
                'temp': cur_temp,
                'desc': weather_description,
                'sunset_time': sunset_time,
                'sunrise_start': sunrise_start,
                'sunset_length': sunset_length,
                'sunrise_end': sunrise_end,
                'sunset_end': sunset_end,
                'sunset_start': sunset_start,
                'day_start': day_start,
                'day_end': day_end
            }
        else:
            self.logger.error(f'Requested data is missing weather section')
