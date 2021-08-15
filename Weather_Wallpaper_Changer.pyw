from logging.handlers import RotatingFileHandler
from threading import Thread
import PySimpleGUIWx as sg
import datetime as dt
import logging as lg
import requests
import random
import ctypes
import json
import time
import os

class Weather:


    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.script_dir)
        
        # logger setup
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.INFO) # Log Level
        my_handler = RotatingFileHandler('Weather_Wallpaper.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)

        with open('weather_types.json') as json_file:
            self.weather_dic = json.load(json_file)
        self.title = 'Weather Wallpaper Changer'
        self.last_wallpaper_run = ''
        self.complete_url = ''
        self.time_of_day = ''
        self.current_weather = ''
        self.skip_wait = False
        self.full_exit = False
        self.pause = False
        # PySimpleGUIWx  and interface tray init
        actions = ['Update Weather', 'Settings', 'Exit']
        self.tray = sg.SystemTray(menu= ['menu', actions], filename='Cloud.ico')
        # wip options
        # TODO add to config
        self.notifications = 0
        self.notif_dur = 5  # duration of notification
        self.notif_frequency = 8  # once every nth weather check.
        self.notif_counter = self.notif_frequency


    def refresh_config(self):
        '''
        Refreshes configuration from config.json
        '''
        with open('config.json') as json_file:
            self.data = json.load(json_file)
        self.api_key = self.data['openweatherapikey']
        self.temp_unit = self.data['temp_unit']
        self.location_mode = self.data['location_mode']
        self.lat = self.data['latitude']
        self.lon = self.data['longitude']
        self.zipcode = self.data['zip_code']
        self.country = self.data['country_code']
        self.check_rate = self.data['check_rate'] * 60


    def create_tray_and_run(self):
        '''
        Initializes Tray and starts main thread.
        '''
        self.run_check_loop()
        default_tray_info = f'{self.title}\nSearching for Weather Data'
        self.tray.update(tooltip=default_tray_info)
        while True:
            event = self.tray.Read()
            print(event)
            if event == 'Pause/Unpause':
                if self.pause is True:
                    self.pause = False
                else:
                    self.pause = True
                    # TODO Set to pause info for tooltip
                    # self.tray.update(tooltip=default_tray_info)
            elif event == 'Exit':
                # FIXME exit somtimes fails to work
                self.skip_wait = 1
                break


    @staticmethod
    def convert_utc(utc):
        '''
        Converts UTC into datetime object.
        '''
        time_list = time.localtime(utc)
        return dt.datetime(*time_list[0:4])


    def create_url(self):
        '''
        Sets up the URL depending on config settings.
        '''
        main_url = 'http://api.openweathermap.org/data/2.5/weather?'
        if self.location_mode == 'coord':  # Sets url to use coordinates
            self.complete_url = f'{main_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}'
        elif self.location_mode == 'zip':  # Sets url to use zip code
            self.complete_url = f'{main_url}zip={self.zipcode},{self.country}&appid={self.api_key}'
        else:
            self.logger.error(f'Missing Location_Mode value in config.')
        self.logger.debug(self.complete_url)
        return self.complete_url


    def check_weather(self):
        '''
        Checks the weather and updates the self.current_weather var with the data.
        '''
        self.create_url()
        self.cur_temp = None
        try:
            response = requests.get(self.complete_url)  # get method of requests module
            data = response.json()  # json method of response object that converts json format data into python dict
        except:
            self.logger.critical('No data found for entered location.')
            default_tray_info = f'{self.title}\nNo Data Found'
            self.tray.update(tooltip=default_tray_info)
            return
        if 'weather' in data:
            weather = data["weather"]  # store the value of "weather" key in variable weather
            self.weather_description = weather[0]["description"]
            if 'temp' in data['main']:
                self.cur_temp = self.convert_temp(data['main']['temp'], self.temp_unit)
            sunset_time = self.convert_utc(data["sys"]['sunset'])
            sunrise_start = self.convert_utc(data["sys"]['sunrise'])
            sunset_length, sunrise_length = 20, 20
            sunrise_end = sunrise_start + dt.timedelta(minutes=sunrise_length, seconds=-1)
            sunset_end = sunset_time + dt.timedelta(seconds=-1)
            sunset_start = sunset_end + dt.timedelta(minutes=-sunset_length) + dt.timedelta(seconds=1)
            day_start = sunrise_end + dt.timedelta(seconds=1)
            day_end = sunset_start + dt.timedelta(seconds=-1)
            # debugging only
            self.logger.debug(f'Sunrise starts at {sunrise_start}')
            self.logger.debug(f'Sunrise ends at {sunrise_end}')
            self.logger.debug(f'Day starts at {day_start}')
            self.logger.debug(f'Day ends at {day_end}')
            self.logger.debug(f'Sunset starts at {sunset_start}')
            self.logger.debug(f'Sunset ends at {sunset_end}')
            # Checks Time of day
            if sunrise_start < dt.datetime.now() < sunrise_end or sunset_start < dt.datetime.now() < sunset_end:
                self.time_of_day = 'Sunset, Sunrise'
            elif day_start < dt.datetime.now() < day_end:
                self.time_of_day = 'Day'
            else:
                self.time_of_day = 'Night'
            if self.weather_description in self.weather_dic:  # converts different OpenWeather data to supported types
                self.current_weather = self.weather_dic[self.weather_description].title()
                self.set_wallpaper()
            else:
                self.logger.warning(f'Unknown weather found - {self.weather_description}')
                print(f'Unknown Weather: Add {self.weather_description} to weather_types.json')
                for item in self.weather_dic:
                    if item in self.weather_description:
                        self.current_weather = self.weather_dic[item].title()
                        self.logger.warning(f'Using {self.current_weather} as possible match')
                        self.set_wallpaper()
        else:
            self.logger.error(f'Requested data is missing weather section')
            # TODO add tray icon notification


    def set_wallpaper(self):
        '''
        Sets Wallpaper based on check_weather function.
        '''
        if f'{self.time_of_day}, {self.current_weather}' != self.last_wallpaper_run:
            wallpaper_list = []
            wallpaper_folder = f'{self.script_dir}\\Wallpaper_Picker_1440'
            for file in os.listdir(f'{wallpaper_folder}\\{self.time_of_day} - {self.current_weather}'):
                wallpaper_list.append(file)
            random_pick = random.randrange(0, len(wallpaper_list))
            path = f"{wallpaper_folder}\\{self.time_of_day} - {self.current_weather}\\{wallpaper_list[random_pick]}"
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
            self.logger.info(f'Wallpaper set to {wallpaper_list[random_pick]}')
            self.last_wallpaper_run = f'{self.time_of_day}, {self.current_weather}'
        else:
            self.logger.info('Wallpaper is already set.')


    @staticmethod
    def convert_temp(temp, unit):
        '''
        Converts given temperature from kelvin into Fahrenheit, Celsius or Kelvin in a nicer to read format.
        '''
        if unit == 'Fahrenheit':
            return f'{round(temp*9/5-459.67, 1)}°F'
        else:
            return f'{round(temp-273.15, 1)}°C'


    def update_tray_text(self):
        '''
        Updates tray text.
        '''
        if self.cur_temp != None:
            msg = f'Time of Day:{self.time_of_day} Weather: {self.current_weather} Temp: {self.cur_temp}'
            weather_info = f'{self.weather_description.title()} | {self.cur_temp}'
        else:
            msg = f'Time of Day:{self.time_of_day} Weather: {self.current_weather}'
            weather_info = f'{self.weather_description.title()}'
        next_check_obj = dt.datetime.now() + dt.timedelta(seconds=int(self.check_rate))
        next_check = f'Next check at {next_check_obj.strftime("%I:%M:%S %p")}'
        self.logger.info(msg)
        info  = f'{self.title}\n{weather_info}\n{next_check}'
        self.tray.update(tooltip=info)
        if self.notifications:
            self.notif_counter -= 1
            if self.notif_counter == 0:
                self.tray.ShowMessage(self.title, info, time=self.notif_dur*1000)
                self.notif_counter = self.notif_frequency


    def run_check_loop(self):
        '''
        Starts main loop function as a thread.
        '''
        def callback():
            while not self.full_exit:
                print('Starting New Loop')
                self.skip_wait = False
                self.refresh_config()
                self.check_weather()
                self.update_tray_text()
                wait_time = self.check_rate
                while not self.skip_wait:
                    # print(self.skip_wait, self.full_exit)
                    wait_time -= 1
                    if wait_time <= 0:
                        self.skip_wait = 1
                    time.sleep(1)
                    while self.pause:
                        pass
                print('Ending Loop')
        weather_thread = Thread(target=callback)
        weather_thread.start()


if __name__ == "__main__":
    Weather().create_tray_and_run()
