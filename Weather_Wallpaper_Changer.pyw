import ctypes, random, json, time, os
from threading import Thread
import PySimpleGUIWx as sg
import datetime as dt
from classes.weather import Weather
from classes.logging import Logger

class Main(Logger):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # json load
    with open('config.json') as json_file:
        data = json.load(json_file)
    api_key = data['openweatherapikey']
    temp_unit = data['temp_unit']
    location_mode = data['location_mode']
    # must have zipcode or lat\lon
    lat = data['latitude']
    lon = data['longitude']
    zipcode = data['zip_code']
    country = data['country_code']
    # check rate
    check_rate = data['check_rate'] * 60
    # init
    weather = Weather(
        api_key=api_key,
        temp_unit=temp_unit,
        zipcode=zipcode,
        country=country,
        lat=lat,
        lon=lon)
    
    with open('weather_types.json') as json_file:
        weather_dic = json.load(json_file)
    title = 'Weather Wallpaper Changer'
    last_wallpaper_run = 'Not yet run'
    current_weather = ''
    full_exit = False
    # PySimpleGUIWx  and interface tray init
    actions = ['Update Weather', 'Settings', 'Exit']
    tray = sg.SystemTray(menu= ['menu', actions], filename='images\Cloud.ico')
    # wip options
    notifications = 0
    notif_dur = 5  # duration of notification
    notif_frequency = 8  # once every nth weather check.
    notif_counter = notif_frequency


    def __init__(self):
        pass


    def create_tray_and_run(self):
        '''
        Initializes Tray and starts main thread.
        '''
        self.run_check_loop()
        default_tray_info = f'{self.title}\nSearching for Weather Data'
        self.tray.update(tooltip=default_tray_info)
        while True:
            event = self.tray.Read()
            if event == 'Exit':
                self.full_exit = True
                break


    def set_wallpaper(self, time_of_day, current_weather):
        '''
        Sets Wallpaper based on check_weather function.
        '''
        if f'{time_of_day}, {current_weather}' != self.last_wallpaper_run:
            wallpaper_list = []
            wallpaper_folder = f'{self.script_dir}\\Wallpaper_Picker_1440'
            for file in os.listdir(f'{wallpaper_folder}\\{time_of_day} - {current_weather}'):
                wallpaper_list.append(file)
            random_pick = random.randrange(0, len(wallpaper_list))
            path = f"{wallpaper_folder}\\{time_of_day} - {current_weather}\\{wallpaper_list[random_pick]}"
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)
            self.logger.info(f'Wallpaper set to {wallpaper_list[random_pick]}')
            self.last_wallpaper_run = f'{time_of_day}, {current_weather}'
        else:
            self.logger.info('Wallpaper is already set.')


    def action(self, weather_dict):
        temp = weather_dict['temp']
        weather_description = weather_dict['desc']
        sunrise_start = weather_dict['sunrise_start']
        sunrise_end =weather_dict['sunrise_end']
        sunset_start = weather_dict['sunset_start']
        sunset_end =weather_dict['sunset_end']
        day_start =weather_dict['day_start']
        day_end =weather_dict['day_end']
        # Checks Time of day
        if sunrise_start < dt.datetime.now() < sunrise_end or sunset_start < dt.datetime.now() < sunset_end:
            time_of_day = 'Sunset, Sunrise'
        elif day_start < dt.datetime.now() < day_end:
            time_of_day = 'Day'
        else:
            time_of_day = 'Night'
        if weather_description in self.weather_dic:  # converts different OpenWeather data to supported types
            current_weather = self.weather_dic[weather_description].title()
            self.set_wallpaper(time_of_day, current_weather)
        else:
            self.logger.warning(f'Unknown weather found - {weather_description}')
            print(f'Unknown Weather: Add {weather_description} to weather_types.json')
            for item in self.weather_dic:
                if item in weather_description:
                    current_weather = self.weather_dic[item].title()
                    self.logger.warning(f'Using {current_weather} as possible match')
                    self.set_wallpaper(time_of_day, current_weather)
        return temp, weather_description, time_of_day, current_weather


    def update_tray_text(self, temp, weather_desc, time_of_day, current_weather):
        '''
        Updates tray text.
        '''
        if temp != None:
            msg = f'Time of Day:{time_of_day} Weather: {current_weather} Temp: {temp}'
            weather_info = f'{weather_desc.title()} | {temp}'
        else:
            msg = f'Time of Day:{time_of_day} Weather: {current_weather}'
            weather_info = f'{weather_desc.title()}'
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
            self.check_rate
            while not self.full_exit:
                weather = self.weather.check(self.location_mode)
                temp, weather_desc, time_of_day, current_weather = self.action(weather)
                self.update_tray_text(temp, weather_desc, time_of_day, current_weather)
                wait_time = self.check_rate
                skip_wait = False
                while not skip_wait:
                    if self.full_exit:
                        break
                    if wait_time <= 0:
                        skip_wait = True
                    wait_time -= 1
                    time.sleep(1)

        weather_thread = Thread(target=callback)
        weather_thread.start()


if __name__ == "__main__":
    Main().create_tray_and_run()
