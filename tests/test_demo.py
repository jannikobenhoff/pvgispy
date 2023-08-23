"""Demonstration tests (see README.md)"""

import unittest
from pprint import pprint
from src.pvgispy import *


class TestDaily(unittest.TestCase):
    def test_call(self):
        daily = Daily(lat=51, lon=9, month=1, preload=True, **{"angle": 0.1, "outputformat": "json"})
        self.assertTrue(daily._params == {'angle': 0.1, "outputformat": "json"}, "Not equal.")

        # daily.fetch_data()
        # pprint(daily.data)

        self.assertTrue(daily.total_irradiance() == 735.3399999999999, "Not equal.")

        print(daily.irradiance())


class TestTMY(unittest.TestCase):
    def test_call(self):
        tmy = TMY(lat=51, lon=9, **{"outputformat": "json"})

        self.assertTrue(tmy._params == {"outputformat": "json"}, "Not equal.")

        pprint(tmy.months_selected())
        pprint(tmy.data["outputs"]["tmy_hourly"][0])
        pprint(tmy.yearly_irradiation())


class TestHourly(unittest.TestCase):
    def test_call(self):
        hourly = Hourly(lat=51, lon=9, pvcalculation=True, loss=20, peakpower=100,
                        angle=0, aspect=-180, startyear=2010, endyear=2011)

        # self.assertTrue(hourly.yearly_pv_production() == 1520203.0, "Not equal.")

        pprint(len(hourly.hourly()))
        pprint(hourly.data["inputs"]["meteo_data"])
        print(hourly.yearly_pv_production())


if __name__ == '__main__':
    unittest.main()
