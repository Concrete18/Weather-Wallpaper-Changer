import json
import re


def validate_entry(entry):
    is_match = False
    patterns = {
        'OpenWeather API Key': r'^[a-zA-Z0-9]{32}$',
        'zip Code': r'^[0-9]{5}$',
        'latitude': r'[0-9.-]',
        'longitude': r'[0-9.-]'}
    while is_match is False:
        string = input(f'What is your {entry}?\n') or 'unset'
        if bool(re.search(patterns[entry], string)) is False:
            print(f'Invalid {entry}.')
        return string


def config_setup():
    '''
    Runs through configuration setup.
    '''
    api = validate_entry('OpenWeather API Key')
    mode = input('Do you want to use zip(1) or coord(2)?\nZip is default if nothing is entered.\n') or 'zip'
    if mode in ['coord', '2', 'coordinates']:
        latitude = validate_entry('latitude')
        longitude = validate_entry('longitude')
        zipcode = 'unset'
    else:
        zipcode = validate_entry('zip Code')
        latitude, longitude = 'unset', 'unset'
    country = input('What is your country code code?\n') or 'us'
    check_rate_per_min = input('How often do you want the wallpaper to update in minutes? 30 is default.\n') or 30
    # dictionary setup
    data = {}
    data['openweatherapikey'] = api
    data['location_mode'] = mode
    data['latitude'] = latitude
    data['longitude'] = longitude
    data['zip_code'] = zipcode
    data['country_code'] = country
    data['check_rate_per_min'] = check_rate_per_min
    # writes to json file
    json_object = json.dumps(data, indent = 4)
    with open('config.json', "w") as outfile:
        outfile.write(json_object)
    input('Config Setup is Complete\nPress Enter to Close.')


if __name__ == '__main__':
    config_setup()
