import unittest
# from unittest import TestCase
import Weather_Wallpaper_Changer

class TestStringMethods(unittest.TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     cls.title = 'Weather Wallpaper Changer'
    #     cls.api_key = 54654651654564
    #     cls.lat, cls.lon = 12, 12
    #     cls.zipcode, cls.country = 31313, 'us'
    #     cls.last_wallpaper_run = ''
    #     cls.complete_url = ''
    #     cls.wait_time = 20 * 60
    #     cls.time_of_day = ''
    #     cls.current_weather = ''


    def test_Create_URL(self):
        # Main = setUpClass(self)
        self.title = 'Weather Wallpaper Changer'
        self.api_key = 54654651654564
        self.lat, self.lon = 12, 12
        self.zipcode, self.country = 31313, 'us'
        self.last_wallpaper_run = ''
        self.complete_url = ''
        self.wait_time = 20 * 60
        self.time_of_day = ''
        self.current_weather = ''
        # Coordinates
        self.location_mode = 'coord'
        self.assertEqual(self.Create_URL(), 'http://api.openweathermap.org/data/2.5/weather?lat=12&lon=12&appid=54654651654564')
        # Zip Code
        self.location_mode = 'zip'
        self.assertEqual(self.Create_URL(), 'http://api.openweathermap.org/data/2.5/weather?zip=31313,us&appid=54654651654564')

    # def test_Weather_Check(self):
    #     self.assertEqual(ww.Weather_Check(), '')


    # def test_Set_Wallpaper(self):
    #     self.assertEqual(ww.Set_Wallpaper(), '')


if __name__ == '__main__':
    unittest.main()
