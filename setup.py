import configparser
import re

Config = configparser.RawConfigParser()


def setup():
    # api = input('What is your OpenWeather API Key?\n') or 'unset'
    mode = input('Do you want to use zip or coord? Zip is Default.\n') or 'zip'
    latitude, latitude, zipcode = 'unset', 'unset', 'unset'
    if mode == 'coord':
        latitude = input('What is your latitude?\n') or 'unset'
        longitude = input('What is your longitude?\n') or 'unset'
        zipcode = 'unset'
    else:
        is_match = False
        while is_match is False:
            zipcode = input('\nWhat is your zip code?\n') or 'unset'
            is_match = bool(re.match(' [0-9]{5} '," "+zipcode+" "))
            if is_match is False:
                print('Invalid Zip Code.')
        latitude, longitude = 'unset', 'unset'
    notifications = input('\nDo you want to turn on notifications for each change?\ny/n\n') or 'yes'
    if notifications == 'n' or 'no':
        notifications = '0'
    else:
        notifications = '1'
    country = input('\nWhat is your country code code?\n') or 'us'
    Config.add_section('Main')
    Config.set('Main', 'openweatherapikey', api)
    Config.set('Main', 'location_mode', mode)
    Config.set('Main', 'weather_notification', notifications)
    Config.set('Main', 'country_code', country)
    Config.set('Main', 'zip_code', zipcode)
    Config.set('Main', 'latitude', latitude)
    Config.set('Main', 'longitude', longitude)
    # with open('Config.ini', 'w') as configfile:
    #     Config.write(configfile)


setup()
