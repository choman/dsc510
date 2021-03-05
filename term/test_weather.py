#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mock
import string
import sys
import unittest
import weather
#import while_loop

from io import StringIO


class TestWindDirection(unittest.TestCase):

    def test_90_directions(self):
        self.assertEqual(weather.getWindDirection(360).split()[0], "N")
        self.assertEqual(weather.getWindDirection(0).split()[0],   "N")
        self.assertEqual(weather.getWindDirection(90).split()[0],  "E")
        self.assertEqual(weather.getWindDirection(180).split()[0], "S")
        self.assertEqual(weather.getWindDirection(270).split()[0], "W")

    def test_45_directions(self):
        self.assertEqual(weather.getWindDirection(45).split()[0],  "NE")
        self.assertEqual(weather.getWindDirection(135).split()[0], "SE")
        self.assertEqual(weather.getWindDirection(225).split()[0], "SW")
        self.assertEqual(weather.getWindDirection(315).split()[0], "NW")

    def test_22_5_directions(self):
        self.assertEqual(weather.getWindDirection(22.5).split()[0],  "NNE")
        self.assertEqual(weather.getWindDirection(67.5).split()[0],  "ENE")
        self.assertEqual(weather.getWindDirection(112.5).split()[0], "ESE")
        self.assertEqual(weather.getWindDirection(157.5).split()[0], "SSE")
        self.assertEqual(weather.getWindDirection(202.5).split()[0], "SSW")
        self.assertEqual(weather.getWindDirection(247.5).split()[0], "WSW")
        self.assertEqual(weather.getWindDirection(292.5).split()[0], "WNW")
        self.assertEqual(weather.getWindDirection(337.5).split()[0], "NNW")

class TestOtherFunctions(unittest.TestCase):

    def test_format_single_word_title(self):
        test_string = "wind"
        expected_string = f" {test_string.title()}:"
        self.assertEqual(weather.format_title(test_string), expected_string)

    def test_format_multi_word_title(self):
        test_string = "wind direction"
        expected_string = f" {test_string.title()}:"
        self.assertEqual(weather.format_title(test_string), expected_string)


    def validate_zip_by_api(self):
        try:
            import uszipcode

        except ModuleNotFoundError:
            return True

        search = uszipcode.SearchEngine(simple_zipcode=True)

        for zip in ["68046", "99999"]:
            a = weather.verifyLocation(zip)
            self.assertEqual(weather.verifyLocation(zip), a)

    def validate_zip_by_url(self):
        weather.USE_USZIPCODE = False

        for zip in ["68046", "99999"]:
            a = weather.verifyLocation(zip)
            self.assertEqual(weather.verifyLocation(zip), a)

    def test_get_state_abbreviation(self):
        for k, v in weather.STATES.items():
            self.assertEqual(weather.getStateAbbreviation(v), k.upper())

    def test_get_city_state(self):
        self.assertEqual(weather.getCityState("Omaha, NE"), ("Omaha", "Ne"))
        self.assertEqual(weather.getCityState("Omaha, NE, US"), ("Omaha", "Ne"))
        
    def test_translate(self):
        test_cities = {
            "st. louis, mo": 'saint louis, mo',
            "st louis, mo": 'saint louis, mo',
            "mt. vernon, va": 'mount vernon, va',
            "ft. calhoun, ne": 'fort calhoun, ne',
            "ft calhoun, ne": 'fort calhoun, ne',
        }
        for k, v in test_cities.items():
            self.assertEqual(weather.translate(k), v)

    def test_request_weather_type(self):
        values = {
            'k': 'standard',
            'c': 'metric',
            'f': 'imperial',
        }

        for k, v in values.items():
            self.assertEqual(weather.requestWeatherType(k), v)
            self.assertEqual(weather.requestWeatherType(k.upper()), v)

    def test_BAD_request_weather_type(self):
        for i in string.ascii_lowercase:
            if i in ['k', 'c', 'f']:
                continue

            self.assertEqual(weather.requestWeatherType(i), 'imperial')
            self.assertEqual(weather.requestWeatherType(i.upper()), 'imperial')

        for i in string.digits:
            self.assertEqual(weather.requestWeatherType(i), 'imperial')

        for i in string.punctuation:
            self.assertEqual(weather.requestWeatherType(i), 'imperial')

class TestWhileLoop(unittest.TestCase):

    def test_city_state(self):
        judge = mock.Mock(side_effect=[1,0])

        out = StringIO()
        sys.stdout = out
        print (weather.requestWeatherLocation("Omaha, NE"))

        self.assertEqual(weather.requestWeatherLocation("Omaha, NE"), "omaha, ne")

if __name__ == "__main__":
    unittest.main()
