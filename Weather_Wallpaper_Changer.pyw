from logging.handlers import RotatingFileHandler
from tkinter import messagebox
import PySimpleGUIWx as sg
import datetime as dt
import logging as lg
import tkinter as tk
import configparser
import subprocess
import threading
import requests
import random
import ctypes
import time
import sys
import os

log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
logFile = f'{os.getcwd()}\\Weather_Wallpaper.log'

my_handler = RotatingFileHandler(logFile, maxBytes=5*1024*1024, backupCount=2)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(lg.INFO)

logger = lg.getLogger(__name__)
logger.setLevel(lg.INFO)
logger.addHandler(my_handler)

root = tk.Tk()
root.withdraw()

Config = configparser.RawConfigParser()
tray = sg.SystemTray(menu= ['menu',['E&xit']], filename='Cloud.ico')

def Write_to_Config():
    with open('Config.ini', 'w') as configfile:
        Config.write(configfile)

class Weather:

    def __init__(self):
        Config.read('Config.ini')
        self.title = 'Weather Wallpaper Changer'
        self.api = Config.get('Main', 'OpenWeatherAPIKey')
        self.location_mode = Config.get('Main', 'Location_Mode')
        self.lat, self.lon = Config.get('Main', 'Latitude'), Config.get('Main', 'Longitude')
        self.zipcode, self.country = Config.get('Main', 'zip_code'), Config.get('Main', 'country_code')
        self.last_wallpaper_run = ''
        self.wait_time = 20 * 60
        self.time_of_day = ''
        self.weather = ''
        self.current_weather = ''

    def Create_Tray(self):
        tray.update(tooltip=self.title)
        while True:
            event = tray.Read()
            # print(event)
            if event == 'Exit':
                sys.exit()

    @staticmethod
    def UTC_Convert(utc):
        time_list = time.localtime(utc)
        converted_time = dt.datetime(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4])
        return converted_time


    def Check_Weather(self):  # Returns Dictionary weather_data
        complete_url = ''
        if self.location_mode == 'coord':
            complete_url = f'http://api.openweathermap.org/data/2.5/weather?'
            f'lat={self.lat}&lon={self.lon}&appid={self.api_key}'
        elif self.location_mode == 'zip':
            complete_url = f'http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.country}&appid={self.api}'
        else:
            logger.error(f'Missing Location_Mode value in config.')
        logger.debug(complete_url)
        try:
            response = requests.get(complete_url)  # get method of requests module
            x = response.json()  # json method of response object that converts json format data into python format data
        except:
            logger.critical('No data found for entered location.')
            sys.exit()
        z = x["weather"]  # store the value of "weather" key in variable z
        weather_description = z[0]["description"]
        sunset_time = self.UTC_Convert(x["sys"]['sunset'])
        sunrise_start = self.UTC_Convert(x["sys"]['sunrise'])
        sunset_length, sunrise_length = 20, 20
        sunrise_end = sunrise_start + dt.timedelta(minutes=sunrise_length, seconds=-1)
        sunset_end = sunset_time + dt.timedelta(seconds=-1)
        sunset_start = sunset_end + dt.timedelta(minutes=-sunset_length) + dt.timedelta(seconds=1)
        day_start = sunrise_end + dt.timedelta(seconds=1)
        day_end = sunset_start + dt.timedelta(seconds=-1)
        logger.debug(f'Sunrise starts at {sunrise_start}')
        logger.debug(f'Sunrise ends at {sunrise_end}')
        logger.debug(f'Day Starts at {day_start}')
        logger.debug(f'Day ends at {day_end}')
        logger.debug(f'Sunset starts at {sunset_start}')
        logger.debug(f'Sunset ends at {sunset_end}')
        # Checks Time of day
        if sunrise_start < dt.datetime.now() < sunrise_end or sunset_start < dt.datetime.now() < sunset_end:
            self.time_of_day = 'Sunset, Sunrise'
        elif day_start < dt.datetime.now() < day_end:
            self.time_of_day = 'Day'
        else:
            self.time_of_day = 'Night'
        weather_list = {
            'clear sky': 'clear sky', 'rain': 'rain', 'light rain': 'rain', 'moderate rain': 'rain',
            'heavy intensity rain': 'rain', 'partly cloudy': 'partly cloudy', 'broken clouds': 'partly cloudy',
            'few clouds': 'partly cloudy', 'scattered clouds': 'partly cloudy', 'overcast clouds': 'overcast',
            'thunderstorm': 'storm', 'haze': 'haze', 'mist': 'haze', 'fog': 'haze'}
        if weather_description in weather_list:
            self.current_weather = weather_list[weather_description].title()
        else:
            logger.warning(f'Unknown weather found - {weather_description}')
            self.current_weather = 'Unknown'


    def Set_Wallpaper(self):  # Sets Wallpaper based on Check_Weather function.
        if self.current_weather == 'Unknown':
            pass
        elif f'{self.time_of_day}, {self.current_weather}' != self.last_wallpaper_run:
            wallpaper_list = []
            wallpaper_folder = f'{os.getcwd()}\\Wallpaper_Picker_1440'
            for file in os.listdir(f'{wallpaper_folder}\\{self.time_of_day} - {self.current_weather}'):
                wallpaper_list.append(file)
            random_pick = random.randrange(0, len(wallpaper_list))
            path = f"{wallpaper_folder}\\{self.time_of_day} - {self.current_weather}\\{wallpaper_list[random_pick]}"
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
            logger.info(f'Wallpaper set to {wallpaper_list[random_pick]}')
            last_wallpaper_run = f'{self.time_of_day}, {self.current_weather}'
        else:
            logger.info('Wallpaper is already set.')


    def Run(self):
        if os.path.exists("Config.ini") is False:
            tk.messagebox.showwarning(title='Setup Helper', message='Config missing.\nRun setup.py and then try again.')
            logger.warning('Config missing. Run setup.py and then try again. ')
            sys.exit()
        while True:
            self.Check_Weather()
            self.Set_Wallpaper()
            logger.info(f'The time of day is {self.time_of_day} and the weather is {self.current_weather}')
            next_check = dt.datetime.now() + dt.timedelta(seconds=self.wait_time)
            tray.update(tooltip=f'{self.title}\nNext check at {next_check.strftime("%I:%M:%S %p")}.')
            time.sleep(self.wait_time)


if __name__ == '__main__':
    Main = Weather()
    weather_thread = threading.Thread(target=Main.Run, daemon=True)
    weather_thread.start()
    Main.Create_Tray()
