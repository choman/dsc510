#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import weather


class TestWindDirection(unittest.TestCase):

    def test_90_directions(self):
        self.assertEqual(weather.getWindDirection(360), "N")
        self.assertEqual(weather.getWindDirection(0),   "N")
        self.assertEqual(weather.getWindDirection(90),  "E")
        self.assertEqual(weather.getWindDirection(180), "S")
        self.assertEqual(weather.getWindDirection(270), "W")

    def test_45_directions(self):
        self.assertEqual(weather.getWindDirection(45),  "NE")
        self.assertEqual(weather.getWindDirection(135), "SE")
        self.assertEqual(weather.getWindDirection(225), "SW")
        self.assertEqual(weather.getWindDirection(315), "NW")

    def test_22_5_directions(self):
        self.assertEqual(weather.getWindDirection(22.5),  "NNE")
        self.assertEqual(weather.getWindDirection(67.5),  "ENE")
        self.assertEqual(weather.getWindDirection(112.5), "ESE")
        self.assertEqual(weather.getWindDirection(157.5), "SSE")
        self.assertEqual(weather.getWindDirection(202.5), "SSW")
        self.assertEqual(weather.getWindDirection(247.5), "WSW")
        self.assertEqual(weather.getWindDirection(292.5), "WNW")
        self.assertEqual(weather.getWindDirection(337.5), "NNW")

    def test_format_single_word_title(self):
        test_string = "wind"
        expected_string = f" {test_string.title()}:"
        self.assertEqual(weather.format_title(test_string), expected_string)

    def test_format_multi_word_title(self):
        test_string = "wind direction"
        expected_string = f" {test_string.title()}:"
        self.assertEqual(weather.format_title(test_string), expected_string)


if __name__ == "__main__":
    unittest.main()
