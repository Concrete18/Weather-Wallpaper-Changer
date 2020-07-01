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

def write_to_config():
    with open('Config.ini', 'w') as configfile:
        Config.write(configfile)

if os.path.exists("Config.ini") is False:
    # subprocess.call(f"{os.getcwd()}/setup.py")
    tk.messagebox.showwarning(title='Setup Helper', message='Config missing.\nRun setup.py and then try again.')
    logger.warning('Config missing. Run setup.py and then try again. ')
    quit()

Config.read('Config.ini')

# Icons made by https://www.flaticon.com/authors/iconixar
tray = sg.SystemTray(menu= ['menu',['Change Location Mode', 'Change Location Info', 'E&xit']], filename='Cloud.ico', tooltip='Weather Wallpaper')

api_key = Config.get('Main', 'OpenWeatherAPIKey')
weather_notification = Config.get('Main', 'weather_notification')
location_mode = Config.get('Main', 'Location_Mode')
latitude, longitude= Config.get('Main', 'Latitude'), Config.get('Main', 'Longitude')
zipcode, country = Config.get('Main', 'zip_code'), Config.get('Main', 'country_code')
last_wallpaper_run = ''

def set_wallpaper(time_of_day, weather, last_run):
    global last_wallpaper_run
    if weather == 'Unknown':
        pass
    elif f'{time_of_day}, {weather}' != last_wallpaper_run:
        wallpaper_list = []
        wallpaper_folder = f'{os.getcwd()}\\Wallpaper_Picker_1440'
        for file in os.listdir(f'{wallpaper_folder}\\{time_of_day} - {weather}'):
            wallpaper_list.append(file)
        random_pick = random.randrange(0, len(wallpaper_list))
        path = f"{wallpaper_folder}\\{time_of_day} - {weather}\\{wallpaper_list[random_pick]}"
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
        logger.info(f'Wallpaper set to {wallpaper_list[random_pick]}')
        last_wallpaper_run = f'{time_of_day}, {weather}'
    else:
        logger.info('Wallpaper is already set.')


def utc_convert(utc):
    time_list = time.localtime(utc)
    converted_time = dt.datetime(time_list[0], time_list[1], time_list[2], time_list[3], time_list[4])
    return converted_time


def current_time_in_range(time1, time2):
    current_time = dt.datetime.now()
    if time1 < current_time < time2:
        return True


def check_weather(lat, lon, location_type, zip_code, country_code):  # Returns Dictionary weather_data
    while True:
        wait_time = 20*60
        print('Weather Check Started')
        complete_url = ''
        if location_mode == 'coord':
            complete_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
        elif location_mode == 'zip':
            complete_url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code},{country_code}&appid={api_key}'
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
        sunset_time = utc_convert(x["sys"]['sunset'])
        sunrise_start = utc_convert(x["sys"]['sunrise'])
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
        current_time = dt.datetime.now()
        # Checks Time of day
        if current_time_in_range(sunrise_start, sunrise_end) or current_time_in_range(sunset_start, sunset_end):
            time_of_day = 'Sunset, Sunrise'
        elif current_time_in_range(day_start, day_end):
            time_of_day = 'Day'
        else:
            time_of_day = 'Night'
        # Checks Weather
        weather_list = {
            'clear sky': 'clear sky', 'rain': 'rain', 'light rain': 'rain', 'moderate rain': 'rain',
            'heavy intensity rain': 'rain', 'partly cloudy': 'partly cloudy', 'broken clouds': 'partly cloudy',
            'few clouds': 'partly cloudy', 'scattered clouds': 'partly cloudy', 'overcast clouds': 'overcast',
            'thunderstorm': 'storm', 'haze': 'haze', 'mist': 'haze', 'fog': 'haze'}
        if weather_description in weather_list:
            current_weather = weather_list[weather_description].title()
        else:
            logger.warning(f'Unknown weather found - {weather_description}')
            current_weather = 'Unknown'
        set_wallpaper(time_of_day, current_weather, last_wallpaper_run)
        if weather_notification:
            tray.ShowMessage('Weather Wallpaper',
            f'It is {time_of_day} and the weather is {weather_description}.\nNext check at {current_time + dt.timedelta(seconds=wait_time)}.')
        logger.info(f'The time of day is {time_of_day} and the weather is {weather_description}')
        next_check = current_time + dt.timedelta(seconds=wait_time)
        converted_check = next_check.strftime("%I:%M:%S %p")
        logger.info(f'Next check at {converted_check}.')
        print(f'Next check at {converted_check}.')
        time.sleep(wait_time)

weather_thread = threading.Thread(target=check_weather, args=(latitude, longitude, location_mode, zipcode, country), daemon=True)
weather_thread.start()

while True:
    event = tray.Read()
    print(event)
    if event == 'Exit':
        quit()
    elif event == 'Change Location Info':
        lat = input('What is your Latitude')
        lon = input('What is your Longitude')
        Config.set('Main', 'latitude', lat)
        latitude = lat
        Config.set('Main', 'longitude', lon)
        Longitude = lon
        write_to_config()
    elif event == 'Change Location Mode':
        mode = ''
        if location_mode == 'coord':
            response = tk.messagebox.askquestion(title='Change Location Mode', message='Want to switch to Zip Code?')
            if response:
                location_mode = 'zip'
        else:
            response = tk.messagebox.askquestion(title='Change Location Mode', message='Want to switch to coordinates?')
            if response:
                location_mode = 'coord'
        Config.set('Main', 'location_mode', location_mode)
        write_to_config()
    elif event == '__DOUBLE_CLICKED__':
        os.system('notepad.exe ' + "Weather_Wallpaper.log")
