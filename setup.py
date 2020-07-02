import configparser
import re

Config = configparser.RawConfigParser()


def validator(entry):
    is_match = False
    while is_match is False:
        string = input(f'\nWhat is your {entry}?\n') or 'unset'
        if entry == 'OpenWeather API Key':
            pattern = r'^[a-zA-Z0-9]{32}$'
        elif entry ==  'Zip Code':
            pattern = r'^[0-9]{5}$'
        else:
            pattern = r'[0-9.-]'
        is_match = bool(re.search(pattern, string))
        if is_match is False:
            print(f'Invalid {entry}.')
    return string


def setup():
    api = validator('OpenWeather API Key')
    mode = input('Do you want to use zip(1) or coord(2)?\nZip is default if nothing is entered.\n') or 'zip'
    latitude, latitude, zipcode = 'unset', 'unset', 'unset'
    if mode == 'coord' or '2':
        latitude, longitude, zipcode = validator('latitude'), validator('longitude'), 'unset'
    else:
        zipcode, latitude, longitude = validator('Zip Code'), 'unset', 'unset'

    country = input('\nWhat is your country code code?\n') or 'us'
    Config.add_section('Main')
    Config.set('Main', 'openweatherapikey', api)
    Config.set('Main', 'location_mode', mode)
    Config.set('Main', 'country_code', country)
    Config.set('Main', 'zip_code', zipcode)
    Config.set('Main', 'latitude', latitude)
    Config.set('Main', 'longitude', longitude)
    with open('Config.ini', 'w') as configfile:
        Config.write(configfile)
    end = input('Config Setup is Complete\nPress Enter to Close.')


setup()
