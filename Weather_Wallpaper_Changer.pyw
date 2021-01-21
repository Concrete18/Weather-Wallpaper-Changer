from logging.handlers import RotatingFileHandler
from threading import Thread
import PySimpleGUIWx as sg
import datetime as dt
import logging as lg
import tkinter as tk
import requests
import random
import ctypes
import json
import time
import os

root = tk.Tk()
root.withdraw()

tray = sg.SystemTray(menu= ['menu',['E&xit']], filename='Cloud.ico')

class Weather:


    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # configuration
        with open('config.json') as json_file:
            self.data = json.load(json_file)
        self.title = 'Weather Wallpaper Changer'
        self.api_key = self.data['openweatherapikey']
        self.location_mode = self.data['location_mode']
        self.lat = self.data['latitude']
        self.lon = self.data['longitude']
        self.zipcode = self.data['zip_code']
        self.country = self.data['country_code']
        self.wait_time = self.data['check_rate_per_min'] * 60
        # var init
        self.last_wallpaper_run = ''
        self.complete_url = ''
        self.time_of_day = ''
        self.current_weather = ''
        # logger setup
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.INFO) # Log Level
        my_handler = RotatingFileHandler('Weather_Wallpaper.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)


    def create_tray_and_run(self):
        '''
        Initializes Tray and starts main thread.
        '''
        self.run_main_loop()
        tray.update(tooltip=self.title)
        while True:
            event = tray.Read()
            print(event)
            if event == 'Exit':
                break


    @staticmethod
    def convert_utc(utc):
        '''
        Converts UTC into datetime object.
        '''
        time_list = time.localtime(utc)
        return dt.datetime(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4])


    def create_url(self):
        '''
        Sets up the URL depending on config settings.
        '''
        main_url = 'http://api.openweathermap.org/data/2.5/weather?'
        if self.location_mode == 'coord':  # Sets url to use coordinates
            self.complete_url = f'{main_url}lat={self.lat}&lon={self.lon}&appid={self.api_key}'
        elif self.location_mode == 'zip':# Sets url to use zip code
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
        try:
            response = requests.get(self.complete_url)  # get method of requests module
            data = response.json()  # json method of response object that converts json format data into python format data
        except:
            self.logger.critical('No data found for entered location.')
            return
        weather = data["weather"]  # store the value of "weather" key in variable z
        weather_description = weather[0]["description"]
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
        # allows converting different OpenWeather types to supported types
        weather_list = {
            'clear sky': 'clear sky', 'rain': 'rain', 'light rain': 'rain', 'moderate rain': 'rain',
            'heavy intensity rain': 'rain', 'very heavy rain': 'rain', 'thunderstorm with heavy rain': 'rain',
            'partly cloudy': 'partly cloudy', 'broken clouds': 'partly cloudy', 'few clouds': 'partly cloudy',
            'scattered clouds': 'partly cloudy', 'overcast clouds': 'overcast','thunderstorm': 'storm', 'haze': 'haze',
            'mist': 'haze', 'fog': 'haze'}
        if weather_description in weather_list:
            self.current_weather = weather_list[weather_description].title()
        else:
            self.logger.warning(f'Unknown weather found - {weather_description}')
            self.current_weather = 'Unknown'


    def set_wallpaper(self):
        '''
        Sets Wallpaper based on check_weather function.
        '''
        if self.current_weather == 'Unknown':
            print('Uknown Weather')
        elif f'{self.time_of_day}, {self.current_weather}' != self.last_wallpaper_run:
            wallpaper_list = []
            wallpaper_folder = f'{os.getcwd()}\\Wallpaper_Picker_1440'
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


    def run_main_loop(self):
        '''
        Starts main loop function as daemon thread.
        '''
        def callback():
            if os.path.exists("config.json") is False:
                tk.messagebox.showwarning(title='Setup Helper', message='Config missing.\nRun setup.py and then try again.')
                self.logger.warning('Config missing. Run setup.py and then try again.')
                return
            while True:
                self.check_weather()
                self.set_wallpaper()
                self.logger.info(f'The time of day is {self.time_of_day} and the weather is {self.current_weather}')
                next_check = dt.datetime.now() + dt.timedelta(seconds=self.wait_time)
                tray.update(tooltip=f'{self.title}\nNext check at {next_check.strftime("%I:%M:%S %p")}.')
                time.sleep(self.wait_time)
        weather_thread = Thread(target=callback, daemon=True)
        weather_thread.start()


if __name__ == "__main__":
    Main = Weather()
    Main.create_tray_and_run()
