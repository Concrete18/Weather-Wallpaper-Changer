import unittest
from Weather_Wallpaper_Changer import Weather

# Work in progress


class TestStringMethods(unittest.TestCase):
    def test_create_url(self):
        Main = Weather()
        # Main = setUpClass(self)
        Main.title = "Weather Wallpaper Changer"
        Main.api_key = 54654651654564
        Main.lat = 12
        Main.lon = 12
        Main.zipcode = 31313
        Main.country = "us"
        Main.complete_url = ""
        # Coordinates
        Main.location_mode = "coord"
        coord_url = "http://api.openweathermap.org/data/2.5/weather?lat=12&lon=12&appid=54654651654564"
        self.assertEqual(Main.create_url(), coord_url)
        # Zip Code
        Main.location_mode = "zip"
        zip_url = "http://api.openweathermap.org/data/2.5/weather?zip=31313,us&appid=54654651654564"
        self.assertEqual(Main.create_url(), zip_url)

    # def test_Weather_Check(self):
    #     self.assertEqual(ww.Weather_Check(), '')

    # def test_Set_Wallpaper(self):
    #     self.assertEqual(ww.Set_Wallpaper(), '')


if __name__ == "__main__":
    unittest.main()
