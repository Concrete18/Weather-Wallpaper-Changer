# Weather Context Control
This is a script that runs in the background setting wallpapers based on the time of day and weather forcast every 20 minutes.
It uses Open Weather to check the sunset and sun rise times and weather. I convert the sunset and sunrise times using code to determine if it is currently sunset or sunrise, 20 minutes each, or if it is night or day.

## Tray Icon
Click the Cloud icon to open the log file.
Right Click to view Edit Configuration and Exit buttons.
Edit Configuration opens the config.ini in notepad.
Exit will close the script.

## Requirements
* Open Weather API Key (Within Config File)
* Coorinates to your location for accuracy.
* PySimpleGUIWx Module
* PythonWx Module
