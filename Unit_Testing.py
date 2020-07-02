import unittest
from tkinter import Tk
import Weather_Wallpaper_Changer as ww


class TestStringMethods(unittest.TestCase):

    def test_CalculateOperation(self):
        self.assertEqual(CalculateAnswer('+', 45, 5), 50)


    def test_CalculateEquation(self):
        self.assertEqual(CalculateEquation([5, '+', 6, '*', 2]), 17, '5+6x2')


if __name__ == '__main__':
    unittest.main()
