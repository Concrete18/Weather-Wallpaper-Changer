from logging.handlers import RotatingFileHandler
from threading import Thread
import PySimpleGUIWx as sg
import datetime as dt
import logging as lg
from tkinter import ttk, messagebox
import tkinter as tk
import subprocess
import requests
import random
import ctypes
import json
import time
import os
import re


class Weather:


    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        # logger setup
        log_formatter = lg.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%m-%d-%Y %I:%M:%S %p')
        self.logger = lg.getLogger(__name__)
        self.logger.setLevel(lg.INFO) # Log Level
        my_handler = RotatingFileHandler('Weather_Wallpaper.log', maxBytes=5*1024*1024, backupCount=2)
        my_handler.setFormatter(log_formatter)
        self.logger.addHandler(my_handler)
        # config init
        self.api_key = ''
        self.temp_unit = ''
        self.location_mode = ''
        self.lat = ''
        self.lon = ''
        self.zipcode = ''
        self.country = ''
        self.check_rate = ''
        # var init
        with open('weather_types.json') as json_file:
            self.weather_dic = json.load(json_file)
        self.title = 'Weather Wallpaper Changer'
        self.last_wallpaper_run = ''
        self.complete_url = ''
        self.time_of_day = ''
        self.current_weather = ''
        # PySimpleGUIWx  and interface tray init
        self.main_gui = tk.Tk()
        actions = ['Update Weather', 'Settings', 'Exit']
        self.tray = sg.SystemTray(menu= ['menu', actions], filename='Cloud.ico')


    @staticmethod
    def validate_entry(entry, string):
        validation = False
        if entry == 'temp_unit':
            if string in ['Fahrenheit', 'Celsius']:
                return True
        elif entry == 'location_mode':
            if string in ['zip', 'coord']:
                return True
        else:
            patterns = {
                'openweatherapikey': r'^[a-zA-Z0-9]{32}$',
                'zip_code': r'^[0-9]{5}$',
                'latitude': r'[0-9.-]',
                'longitude': r'[0-9.-]',
                'country_code': r'[a-zA-Z]{2}',
                'check_rate': r'[0-9]'}
            validation = bool(re.search(patterns[entry], string))
        return validation


    def save_to_config(self):
        data = {}
        data['openweatherapikey'] = self.api_entry.get()
        data['temp_unit'] = self.temp_unit.get()
        data['location_mode'] = self.location_mode.get()
        data['latitude'] = self.lat_entry.get()
        data['longitude'] = self.lon_entry.get()
        data['zip_code'] = self.zip_entry.get()
        data['country_code'] = self.country_code_entry.get()
        data['check_rate'] = int(self.check_rate_entry.get())
        for entry, string in data.items():
            print(entry, string)
            if self.validate_entry(entry, string) is False:
                print('feck')
                return
            # writes to json file
        input()
        json_object = json.dumps(data, indent = 4)
        with open('config.json', "w") as outfile:
            outfile.write(json_object)
            input('\nConfig Setup is Complete.\nPress Enter to Continue.')


    def create_setup_window(self):
        # Defaults
        BoldBaseFont = "Aria;"
        self.main_gui.iconbitmap(self.main_gui, 'Cloud.ico')
        self.main_gui.title('Weather Wallpaper Changer')
        self.main_gui.resizable(width=False, height=False)

        # window_width = 670
        # window_height = 550
        # self.tk_window_options(self.main_gui, window_width, window_height)
        # self.main_gui.geometry(f'{window_width}x{window_height}+{width}+{height}')

        info_text = 'Settings'
        Title = tk.Label(self.main_gui, text=info_text, font=(BoldBaseFont, 15))
        Title.grid(columnspan=4, row=0, pady=5)

        Setup_Frame = tk.Frame(self.main_gui)
        Setup_Frame.grid(columnspan=4, row=3, padx=15, pady=(0, 10))

        pad_y = 10
        entry_width = 35
        api_label = ttk.Label(Setup_Frame, text='API Key')
        api_label.grid(row=0, column=0)
        self.api_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.api_entry.grid(row=0, column=1, columnspan=3, pady=pad_y, padx=10)

        self.temp_unit = tk.StringVar()
        temp_unit__label = ttk.Label(Setup_Frame, text='Unit of\nTemp')
        temp_unit__label.grid(row=1, column=0)
        fahrenheit_radio = ttk.Radiobutton (Setup_Frame, text='°F', value='Fahrenheit', variable=self.temp_unit)
        fahrenheit_radio.grid(row=1, column=1, pady=pad_y, padx=10, sticky='W')
        celsius_radio = ttk.Radiobutton (Setup_Frame, text='°C', value='Celsius', variable=self.temp_unit)
        celsius_radio.grid(row=1, column=2, pady=pad_y, padx=10, sticky='W')

        self.location_mode = tk.StringVar()
        loc_mode_label = ttk.Label(Setup_Frame, text='Location\nMode')
        loc_mode_label.grid(row=2, column=0)
        loc_mode_zip = ttk.Radiobutton (Setup_Frame, text='Zip Code', value='zip', variable=self.location_mode)
        loc_mode_zip.grid(row=2, column=1, pady=pad_y, padx=10, sticky='W')
        loc_mode_coord = ttk.Radiobutton (Setup_Frame, text='Coordinates', value='coord', variable=self.location_mode)
        loc_mode_coord.grid(row=2, column=2, pady=pad_y, padx=10, sticky='W')

        lat_label = ttk.Label(Setup_Frame, text='Latitude')
        lat_label.grid(row=3, column=0)
        self.lat_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.lat_entry.grid(row=3, column=1, columnspan=3, pady=pad_y, padx=10)

        lon_label = ttk.Label(Setup_Frame, text='Longitude')
        lon_label.grid(row=4, column=0)
        self.lon_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.lon_entry.grid(row=4, column=1, columnspan=3, pady=pad_y, padx=10)

        zip_label = ttk.Label(Setup_Frame, text='Zip Code')
        zip_label.grid(row=5, column=0)
        self.zip_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.zip_entry.grid(row=5, column=1, columnspan=3, pady=pad_y, padx=10)

        country_code_label = ttk.Label(Setup_Frame, text='Country Code')
        country_code_label.grid(row=6, column=0)
        self.country_code_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.country_code_entry.grid(row=6, column=1, columnspan=3, pady=pad_y, padx=10)

        check_rate_label = ttk.Label(Setup_Frame, text='Check Rate')
        check_rate_label.grid(row=7, column=0)
        self.check_rate_entry = ttk.Spinbox(Setup_Frame, width=5, from_=1, to=1000)
        self.check_rate_entry.grid(row=7, column=1, columnspan=1, pady=pad_y, padx=10, sticky='W')

        save_button = ttk.Button(Setup_Frame, text='Save', command=self.save_to_config)
        save_button.grid(row=8, columnspan=4, pady=5)

        if not os.path.exists("config.json"):
            # creates config if it does not exist
            data = {
                "openweatherapikey": "Insert API Key",
                "temp_unit": "Fahrenheit",
                "location_mode": "zip",
                "latitude": "Insert latitude if coord is selected",
                "longitude": "Insert longitude if coord is selected",
                "zip_code": "Insert zip code if zip code is selected",
                "country_code": "Insert Country Code, USA is US",
                "check_rate": 30}
            json_object = json.dumps(data, indent = 4)
            with open('config.json', "w") as outfile:
                outfile.write(json_object)
        # opens config if it exists or after it is created
        with open('config.json') as json_file:
            self.data = json.load(json_file)
        self.api_entry.insert(0, self.data['openweatherapikey'])
        self.temp_unit.set(self.data['temp_unit'])
        self.location_mode.set(self.data['location_mode'])
        self.lat_entry.insert(0, self.data['latitude'])
        self.lon_entry.insert(0, self.data['longitude'])
        self.zip_entry.insert(0, self.data['zip_code'])
        self.country_code_entry.insert(0, self.data['country_code'])
        self.check_rate_entry.insert(0, self.data['check_rate'])

        self.main_gui.mainloop()


    def refresh_config(self):
        '''
        Refreshes configuration from config.json
        '''
        self.api_key = self.data['openweatherapikey']
        self.temp_unit = self.data['temp_unit']
        self.location_mode = self.data['location_mode']
        self.lat = self.data['latitude']
        self.lon = self.data['longitude']
        self.zipcode = self.data['zip_code']
        self.country = self.data['country_code']
        self.check_rate = self.data['check_rate'] * 60


    def config_check(self):
        '''
        Checks for existing config file.
        '''
        if not os.path.exists("config.json"):
            root = tk.Tk()
            root.withdraw()
            if messagebox.askyesno(title=self.title, message='Config is missing.\nDo you want to run setup?'):
                self.create_setup_window()
            else:
                self.logger.warning('Config is missing. Run setup.py and then try again.')
            exit()
        # configuration
        with open('config.json') as json_file:
            self.data = json.load(json_file)
        if 'Insert' in self.data['openweatherapikey']:
            self.create_setup_window()
        try:
            self.refresh_config()
        except KeyError:
            root = tk.Tk()
            root.withdraw()
            msg = 'Config is corrupted.\nDo you want to open settings to view config'
            if messagebox.askyesno(title=self.title, message=msg):
                subprocess.Popen(["python", 'setup.py'], shell=False)
            else:
                self.logger.warning('Config is corrupted. Run setup.py again and then try again.')
            exit()


    def create_tray_and_run(self):
        '''
        Initializes Tray and starts main thread.
        '''
        self.run_main_loop()
        default_tray_info = f'{self.title}\nSearching for Weather Data'
        self.tray.update(tooltip=default_tray_info)
        while True:
            event = self.tray.Read()
            print(event)
            if event == 'Pause/Unpause':
                # TODO Add pausing and fix seperate functions
                pass
            elif event == 'Update Weather':
                self.check_weather()
            elif event == 'Settings':
                self.create_setup_window()
                self.refresh_config()
                print(self.location_mode)
            elif event == 'Exit':
                exit()


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
            root = tk.Tk()
            root.withdraw()
            msg = f'Requested data appears to be missing the weather dictionary which is required.\n\n{data}'
            messagebox.showwarning(title=self.title, message=msg)


    def set_wallpaper(self):
        '''
        Sets Wallpaper based on check_weather function.
        '''
        if f'{self.time_of_day}, {self.current_weather}' != self.last_wallpaper_run:
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


    @staticmethod
    def convert_temp(temp, unit):
        '''
        Converts given temperature from kelvin into Fahrenheit, Celsius or Kelvin in a nicer to read format.
        '''
        if unit == 'Fahrenheit':
            return f'{round(temp*9/5-459.67, 1)}°F'
        else:
            return f'{round(temp-273.15, 1)}°C'


    def run_main_loop(self):
        '''
        Starts main loop function as daemon thread.
        '''
        def callback():
            while True:
                self.check_weather()
                if self.cur_temp != None:
                    msg = f'Time of Day:{self.time_of_day} Weather: {self.current_weather} Temp: {self.cur_temp}'
                    weather_info = f'{self.weather_description.title()} | {self.cur_temp}'
                else:
                    msg = f'Time of Day:{self.time_of_day} Weather: {self.current_weather}'
                    weather_info = f'{self.weather_description.title()}'
                next_check_obj = dt.datetime.now() + dt.timedelta(seconds=self.check_rate)
                next_check = f'Next check at {next_check_obj.strftime("%I:%M:%S %p")}'
                self.logger.info(msg)
                self.tray.update(tooltip=f'{self.title}\n{weather_info}\n{next_check}')
                time.sleep(self.check_rate)
        weather_thread = Thread(target=callback, daemon=True)
        weather_thread.start()


if __name__ == "__main__":
    Main = Weather()
    Main.config_check()
    Main.create_tray_and_run()
