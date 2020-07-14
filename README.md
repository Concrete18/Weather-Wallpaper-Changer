# Weather Context Control
This is a script that runs in the background setting wallpapers based on the time of day and weather forecast every 20 minutes.
It uses Open Weather to check the sunset and sun rise times and weather. I convert the sunset and sunrise times using code to determine if it is currently sunset or sunrise, 20 minutes each, or if it is night or day.

## Tray Icon
* Hover over the icon to see the next time the script will run.
* Exit will close the script.

Icons made by https://www.flaticon.com/authors/iconixar

## First Time Start up
Run the setup.py first to generate your Config.ini file.
It will ask questions for you to create it so you won't have to edit any configs yourself.
Have your Openweather API Key and zip code or coordinates ready.

```ini
[Main]
openweatherapikey = API_Key
location_mode = zip
country_code = Example:'us'
zip_code = 5 digit zip
latitude = coordinates
longitude = coordinates
```

## Module Requirements
### Run within your normal console for pip.
```
pip install -r requirements.txt
```
* Open Weather API Key (Within Config File)
* Requests Module
* PySimpleGUIWx Module
* PythonWx Module

## Python Techniques Used
* Tkinter messageboxes
* Logging
* Requests is used to acquire weather data to generate time information via a REST API
* Full use of an Openweather API
* Config.ini file using configparser
* Task bar interface using PySimpleGUIWx Module
* Threading to allow timers/main tasks to run simultaneously with the taskbar
