# Weather Context Control

This is a script that runs in the background setting wallpapers based on the time of day and weather forecast every 20 minutes.
It uses Open Weather to check the sunset and sun rise times and weather. I convert the sunset and sunrise times using code to determine if it is currently sunset or sunrise, 20 minutes each, or if it is night or day.

## Tray Icon

* Hover over the icon to see the next time the script will run.
* Exit will close the script.

Icons made by [iconixar on flaticon](https://www.flaticon.com/authors/iconixar").

## First Time Start up

Run the setup&#46;py first to generate your Config.json file.
It will ask questions for you to create it so you won't have to edit any configs yourself.
Have your Openweather API Key ready and your zip code or coordinates as well.

```json
{
    "openweatherapikey": "insert_api_key",
    "location_mode": "coord",
    "country_code": "us",
    "zip_code": "5 digit zip code",
    "latitude": "coordinates",
    "longitude": "coordinates",
    "check_rate_per_min": 20
}
```

## Module Requirements

Run within your normal console for pip

```git
pip install -r requirements.txt
```

* Open Weather API Key (Within Config File)
* Requests Module
* PySimpleGUIWx Module
* PythonWx Module

## Planned Features and Fixes

* Fix Taskbar being wrong after waking from sleep.

## Python Techniques Used

* Tkinter messageboxes
* Logging
* Requests is used to acquire weather data to generate time information via a REST API
* Full use of an Openweather API
* Config.json file using json
* Task bar interface using PySimpleGUIWx Module
* Threading to allow timers/main tasks to run simultaneously with the taskbar
