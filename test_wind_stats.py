import time
from unittest import TestCase

from wind_stats import WindStats


class TestWindStats(TestCase):
    def setUp(self):
        self.wind_stats = WindStats()



    def test_add_wind_reading_empty(self):
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
        print(int(time.time()))
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


