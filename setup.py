from tkinter import ttk
import tkinter as Tk
import json
import re
import os


class setup_config:


    def __init__(self):
        self.main_gui = Tk.Tk()


    @staticmethod
    def validate_entry(entry, string):
        patterns = {
            'openweatherapikey': r'^[a-zA-Z0-9]{32}$',
            'temp_unit': r'^[a-zA-Z]$',
            'location_mode': r'^[a-zA-Z]$',
            'zip_code': r'^[0-9]{5}$',
            'latitude': r'[0-9.-]',
            'longitude': r'[0-9.-]',
            'country_code Code': r'[a-zA-Z]{2,3}',
            'check_rate': r'[0-9]'}
        return bool(re.search(patterns[entry], string))


    def save_to_config(self):
        data = {}
        data['openweatherapikey'] = self.api_entry.get()
        data['temp_unit'] = self.temp_unit_entry.get()
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
        Title = Tk.Label(self.main_gui, text=info_text, font=(BoldBaseFont, 15))
        Title.grid(columnspan=4, row=0, pady=5)

        Setup_Frame = Tk.Frame(self.main_gui)
        Setup_Frame.grid(columnspan=4, row=3, padx=15, pady=(0, 10))

        pad_y = 10
        entry_width = 35
        api_label = ttk.Label(Setup_Frame, text='API Key')
        api_label.grid(row=0, column=0)
        self.api_entry = ttk.Entry(Setup_Frame, width=entry_width, exportselection=0)
        self.api_entry.grid(row=0, column=1, columnspan=3, pady=pad_y, padx=10)

        self.temp_unit = Tk.StringVar()
        temp_unit__label = ttk.Label(Setup_Frame, text='Unit of\nTemp')
        temp_unit__label.grid(row=1, column=0)
        fahrenheight_radio = ttk.Radiobutton (Setup_Frame, text='°F', value='Fahrenheight', variable=self.temp_unit)
        fahrenheight_radio.grid(row=1, column=1, pady=pad_y, padx=10, sticky='W')
        celsius_radio = ttk.Radiobutton (Setup_Frame, text='°C', value='Celsius', variable=self.temp_unit)
        celsius_radio.grid(row=1, column=2, pady=pad_y, padx=10, sticky='W')

        self.location_mode = Tk.StringVar()
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
                "temp_unit": "Fahrenheight",
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


if __name__ == '__main__':
    App = setup_config()
    App.create_setup_window()
