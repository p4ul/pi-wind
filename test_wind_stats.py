import time
from random import random
from unittest import TestCase

from collections import deque

from wind_stats import WindStats, WindReading, MAX_QUEUE_LENGTH


class TestWindStats(TestCase):
    def setUp(self):
        self.wind_stats = WindStats()

    def test_add_wind_reading_empty(self):
        self.wind_stats.reset_data()
        self.wind_stats.add_wind_reading(time.time(), 0, 0)
        expected = "&winddir=0.0" \
                   "&windspeedmph=0.0" \
                   "&windgustmph=0.0" \
                   "&windgustdir=0.0" \
                   "&windspdmph_avg2m=0.0" \
                   "&winddir_avg2m=0.0" \
                   "&windgustmph_10m=0.0" \
                   "&windgustdir_10m=0.0"
        self.assertEqual(self.wind_stats.to_get_variables(), expected)

    def test_add_wind_reading_1_point(self):
        self.wind_stats.reset_data()

        self.wind_stats.add_wind_reading(time.time(), 1.0, 22.5)

        expected = "&winddir=22.5" \
                   "&windspeedmph=1.0" \
                   "&windgustmph=1.0" \
                   "&windgustdir=22.5" \
                   "&windspdmph_avg2m=1.0" \
                   "&winddir_avg2m=22.5" \
                   "&windgustmph_10m=1.0" \
                   "&windgustdir_10m=22.5"
        self.assertEqual(self.wind_stats.to_get_variables(), expected)

    def test_windspdmph_avg2m(self):
        self.wind_stats.reset_data()

        # record data every 5 seconds for 2 minutes
        period = int((60 * 2) / 5)
        for i in range(period):
            if i < int(period/2):
                self.wind_stats.add_wind_reading(time.time(), 11.0, 180)
            else:
                self.wind_stats.add_wind_reading(time.time(), 1.0, 0)

        expected = "&winddir=0.0" \
                   "&windspeedmph=1.0" \
                   "&windgustmph=11.0" \
                   "&windgustdir=180.0" \
                   "&windspdmph_avg2m=6.0" \
                   "&winddir_avg2m=90.0" \
                   "&windgustmph_10m=11.0" \
                   "&windgustdir_10m=180.0"
        self.assertEqual(self.wind_stats.to_get_variables(), expected)

    def windgust_10m(self):
        self.wind_stats.reset_data()
        # start 10 mins ago
        test_time = time.time() - (60*10)

        # add big gust
        self.wind_stats.add_wind_reading(test_time, 111.0, 22.5)
        test_time += 5

        # record data every 5 seconds for 2 minutes
        period = int((60 * 10) / 5)
        for i in range(period):
            if i < int(period-120):
                self.wind_stats.add_wind_reading(test_time, 11.0, 180)
            elif i < int((period-120/2)):
                self.wind_stats.add_wind_reading(test_time, 1.0, 0)
            else:
                self.wind_stats.add_wind_reading(test_time, round(random() * 100, 1), round(random() * 100, 1))
            test_time += 5

        expected = "&winddir=0.0" \
                   "&windspeedmph=1.0" \
                   "&windgustmph=11.0" \
                   "&windgustdir=180.0" \
                   "&windspdmph_avg2m=6.0" \
                   "&winddir_avg2m=90.0" \
                   "&windgustmph_10m=111.0" \
                   "&windgustdir_10m=22.5"
        self.assertEqual(self.wind_stats.to_get_variables(), expected)


    # only last 120 points should be kept
    def test_add_wind_reading_300_points(self):
        self.wind_stats.reset_data()
        test_time = time.time()

        for i in range(150):
            self.wind_stats.add_wind_reading(test_time, round(random() * 100, 1), round(random() * 100, 1))

        self.assertEqual(MAX_QUEUE_LENGTH, self.wind_stats.data_length())
