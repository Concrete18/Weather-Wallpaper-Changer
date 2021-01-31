import json
import re


def validate_entry(entry):
    patterns = {
        'OpenWeather API Key': r'^[a-zA-Z0-9]{32}$',
        'zip Code': r'^[0-9]{5}$',
        'latitude': r'[0-9.-]',
        'longitude': r'[0-9.-]'}
    while True:
        string = input(f'\nWhat is your {entry}?\n') or 'unset'
        if bool(re.search(patterns[entry], string)) is False:
            print(f'Invalid {entry}.')
            continue
        return string


def config_setup():
    '''
    Runs through configuration setup.
    '''
    api = validate_entry('OpenWeather API Key')
    temp_unit = input('\nEnter a unit of temperature\nType Fahrenheit, Celcius or Kelvin.\n')[0].lower() or 'f'
    if temp_unit not in ['f', 'c', 'k']:
        temp_unit = 'f'
        print('Unknown unit, defaulting to Fahrenheit')
    mode = input('\nDo you want to use zip(1) or coord(2)?\nZip is default if nothing is entered.\n') or 'zip'
    if mode in ['coord', '2', 'coordinates']:
        latitude = validate_entry('latitude')
        longitude = validate_entry('longitude')
        zipcode = 'unset'
    else:
        zipcode = validate_entry('zip Code')
        latitude, longitude = 'unset', 'unset'
    country = input('\nWhat is your country code code?\n') or 'us'
    check_rate_per_min = input('\nHow often do you want the wallpaper to update in minutes? 30 is default.\n') or 30
    # dictionary setup
    data = {}
    data['openweatherapikey'] = api
    data['temp_unit'] = temp_unit
    data['location_mode'] = mode
    data['latitude'] = latitude
    data['longitude'] = longitude
    data['zip_code'] = zipcode
    data['country_code'] = country
    data['check_rate_per_min'] = check_rate_per_min
    for type, entry in data.items():
        print(f'{type}: {entry}')
    if input('\nIs this correct?\n') in ['yes', 'y', 'yeah']:
        # writes to json file
        json_object = json.dumps(data, indent = 4)
        with open('config.json', "w") as outfile:
            outfile.write(json_object)
        input('Config Setup is Complete\nPress Enter to Close.')
    else:
        print('Starting Over\n')
        config_setup()


if __name__ == '__main__':
    config_setup()
