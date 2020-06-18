import configparser

Config = configparser.RawConfigParser()


def write_to_config():
    with open('Config.ini', 'w') as configfile:
        Config.write(configfile)

def setup():
    api = input('What is your OpenWeather API Key?\n') or 'unset'
    mode = input('Do you want to use zip or coord?\n') or 'zip'
    latitude, latitude, zipcode = 'unset', 'unset', 'unset'
    if mode ==  'zip':
        zipcode = input('What is your zip code\n?') or 'unset'
        latitude, longitude = 'unset', 'unset'
    elif mode  ==  'coord':
        latitude = input('What is your latitude?\n') or 'unset'
        longitude = input('What is your longitude?\n') or 'unset'
        zipcode = 'unset'
    notifications = input('Do you want to turn on notifications for each change?\ny/n\n') or 'yes'
    if notifications == 'n' or 'no':
        notifications = 0
    else:
        notifications = 1
    country = input('What is your country code code?\n') or 'us'
    Config.add_section('Main')
    Config.set('Main', 'openweatherapikey', api)
    Config.set('Main', 'location_mode', mode)
    Config.set('Main', 'weather_notification', notifications)
    Config.set('Main', 'country_code', country)
    Config.set('Main', 'zip_code', zipcode)
    Config.set('Main', 'latitude', latitude)
    Config.set('Main', 'longitude', longitude)
    write_to_config()

setup()