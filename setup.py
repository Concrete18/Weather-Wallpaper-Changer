import subprocess
import json
import re


def validate_entry(entry):
    patterns = {
        'OpenWeatherMap.org API Key': r'^[a-zA-Z0-9]{32}$',
        'zip Code': r'^[0-9]{5}$',
        'latitude': r'[0-9.-]',
        'longitude': r'[0-9.-]',
        'Country Code: Example US': r'[a-zA-Z]{2,3}',
        'How frequently do you want the weather and wallpaper to update in minutes?': r'[0-9]'}
    string = ''
    while not bool(re.search(patterns[entry], string)):
        string = input(f'\nWhat is your {entry}?\n') or 'unset'
    return string


def config_setup():
    '''
    Runs through configuration setup.
    '''
    api = validate_entry('OpenWeatherMap.org API Key')
    # unit of temp
    temp_unit=''
    while temp_unit not in ['f', 'c', 'k']:
        temp_unit = input('\nEnter a unit of temperature\nType Fahrenheit, Celcius or Kelvin.\n')[0].lower() or 'f'
    # location mode
    mode = ''
    while mode not in ['coord', '2', 'coordinates', 'zip', '1', 'zip code']:
        mode = input('\nDo you want to use zip(1) or coord(2)?\nZip is default if nothing is entered.\n') or 'zip'
    country = 'unset'
    if mode in ['coord', '2', 'coordinates']:  # coordinates mode
        latitude = validate_entry('latitude')
        longitude = validate_entry('longitude')
        zipcode = 'unset'
    else:  # zip code mode
        zipcode = validate_entry('zip Code')
        latitude, longitude = 'unset', 'unset'
        country = validate_entry('Country Code: Example US')
    check_rate_per_min = validate_entry('How frequently do you want the weather and wallpaper to update in minutes?')
    # dictionary setup
    data = {}
    data['openweatherapikey'] = api
    data['temp_unit'] = temp_unit
    data['location_mode'] = mode
    data['latitude'] = latitude
    data['longitude'] = longitude
    data['zip_code'] = zipcode
    data['country_code'] = country
    data['check_rate_per_min'] = int(check_rate_per_min)
    for type, entry in data.items():
        print(f'\n{type}: {entry}')
    if input('\nIs this correct? Y\\N\n').lower() in ['yes', 'y', 'yeah']:
        # writes to json file
        json_object = json.dumps(data, indent = 4)
        with open('config.json', "w") as outfile:
            outfile.write(json_object)
        input('\nConfig Setup is Complete.\nPress Enter to Continue.')
    else:
        print('Starting Over\n')


if __name__ == '__main__':
    config_setup()
