import unittest
from Weather_Wallpaper_Changer import Weather

# Work in progress

class TestStringMethods(unittest.TestCase):


    def test_create_url(self):
        Main = Weather()
        # Main = setUpClass(self)
        Main.title = 'Weather Wallpaper Changer'
        Main.api_key = 54654651654564
        Main.lat = 12
        Main.lon = 12
        Main.zipcode = 31313
        Main.country = 'us'
        Main.complete_url = ''
        # Coordinates
        Main.location_mode = 'coord'
        coord_url = 'http://api.openweathermap.org/data/2.5/weather?lat=12&lon=12&appid=54654651654564'
        self.assertEqual(Main.create_url(), coord_url)
        # Zip Code
        Main.location_mode = 'zip'
        zip_url = 'http://api.openweathermap.org/data/2.5/weather?zip=31313,us&appid=54654651654564'
        self.assertEqual(Main.create_url(), zip_url)


    def test_validate_entry(self):
        Main = Weather()
        # api key
        self.assertTrue(Main.validate_entry('openweatherapikey', 'ebb08232da61e5c0sht76563a5hf7637'))
        self.assertFalse(Main.validate_entry('openweatherapikey', '31820'))
        self.assertFalse(Main.validate_entry('openweatherapikey', '%bb08232da61e5c0sht76563a5hf7637'))
        self.assertFalse(Main.validate_entry('openweatherapikey', 'ebb08232da61e5c0sht76563a5hf763'))
        # temp unit
        self.assertTrue(Main.validate_entry('temp_unit', 'Fahrenheit'))
        self.assertTrue(Main.validate_entry('temp_unit', 'Celsius'))
        self.assertFalse(Main.validate_entry('temp_unit', 'Fahrenheight'))
        self.assertFalse(Main.validate_entry('temp_unit', '1584525212sdas'))
        # location mode
        self.assertTrue(Main.validate_entry('location_mode', 'zip'))
        self.assertTrue(Main.validate_entry('location_mode', 'coord'))
        self.assertFalse(Main.validate_entry('location_mode', 'this is wrong'))
        # latitude
        self.assertTrue(Main.validate_entry('latitude', '-12.25'))
        self.assertFalse(Main.validate_entry('latitude', 'this is wrong'))
        # longitude
        self.assertTrue(Main.validate_entry('longitude', '12'))
        self.assertFalse(Main.validate_entry('longitude', 'this is wrong'))
        # zip code
        self.assertTrue(Main.validate_entry('zip_code', '12345'))
        self.assertTrue(Main.validate_entry('zip_code', 12345))
        self.assertFalse(Main.validate_entry('zip_code', 1234567))
        self.assertFalse(Main.validate_entry('zip_code', 'this is wrong'))
        # country code
        self.assertTrue(Main.validate_entry('country_code', 'us'))
        self.assertFalse(Main.validate_entry('country_code', 'this is wrong'))
        self.assertFalse(Main.validate_entry('country_code', 'ussssss'))
        # check rate
        self.assertTrue(Main.validate_entry('check_rate', 20))
        self.assertTrue(Main.validate_entry('check_rate', '20'))

    # def test_Weather_Check(self):
    #     self.assertEqual(ww.Weather_Check(), '')


    # def test_Set_Wallpaper(self):
    #     self.assertEqual(ww.Set_Wallpaper(), '')


if __name__ == '__main__':
    unittest.main()
