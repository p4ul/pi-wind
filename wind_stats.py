import time
from collections import deque, namedtuple

from settings import time_between_updates

WindReading = namedtuple('WindReading', ['time', 'speedmph', 'direction'])

# 120 slots is equal to 10 mins at 5 second intervals
MAX_QUEUE_LENGTH = 120


class WindStats:
    # A queue of WindReading tuples
    __data = deque([], MAX_QUEUE_LENGTH)

    def results_after_timestamp(self, after_time):
        return filter(lambda windReading: windReading.time >= after_time, self.__data)

    # [0 - 360 instantaneous wind direction]
    def winddir(self):
        return self.__data[-1].direction

    # [mph instantaneous wind speed]
    def windspeedmph(self):
        return self.__data[-1].speedmph

    # Finds the highest gust (speed & direction) since the last poll
    # returns:
    # windgustmph [mph current wind gust, using software specific time period]:
    # windgustdir[0 - 360 using software specific time period]
    def windgust(self):
        after_time = int(time.time() - time_between_updates)
        results = self.results_after_timestamp(after_time)

        highest_windgust = max(results, key=lambda wind_reading: wind_reading.speedmph)
        return highest_windgust.speedmph, highest_windgust.direction

    # windspdmph_avg2m [mph 2 minute average wind speed mph]
    # winddir_avg2m [0 - 360 2 minute average wind direction]f):
    def windspdmph_avg2m(self):
        after_time = int(time.time() - (60 * 2))
        results2m = list(self.results_after_timestamp(after_time))

        windspdmph_avg2m_raw = list(map(lambda wind_reading: wind_reading.speedmph, results2m))
        windspdmph_avg2m = sum(windspdmph_avg2m_raw) / len(windspdmph_avg2m_raw)

        winddir_avg2m_raw = list(map(lambda wind_reading: wind_reading.direction, results2m))
        winddir_avg2m = sum(winddir_avg2m_raw) / len(winddir_avg2m_raw)

        return windspdmph_avg2m, winddir_avg2m

    # Finds the highest gust (speed & direction) in last 10mins
    # returns:
    # windgustmph [mph past 10 minutes wind gust mph]
    # windgustdir [0 - 360 past 10 minutes wind gust direction]
    def windgust_10m(self):
        after_time = int(time.time() - (60 * 10))
        results10m = self.results_after_timestamp(after_time)

        highest_windgust = max(results10m, key=lambda wind_reading: wind_reading.speedmph)
        return highest_windgust.speedmph, highest_windgust.direction

    def data_length(self):
        return len(self.__data)

    def reset_data(self):
        self.__data.clear()

    def add_wind_reading(self, current_time, speedmph, direction):
        self.__data.append(WindReading(current_time, speedmph, direction))

    def to_get_variables(self):
        windgustmph, windgustdir = self.windgust()
        windgustmph_10m, windgustdir_10m = self.windgust_10m()
        windspdmph_avg2m, winddir_avg2m = self.windspdmph_avg2m()

        return "&winddir=%.1f" \
               "&windspeedmph=%.1f" \
               "&windgustmph=%.1f" \
               "&windgustdir=%.1f" \
               "&windspdmph_avg2m=%.1f" \
               "&winddir_avg2m=%.1f" \
               "&windgustmph_10m=%.1f" \
               "&windgustdir_10m=%.1f" % (
                   self.winddir(),
                   self.windspeedmph(),
                   windgustmph,
                   windgustdir,
                   windspdmph_avg2m,
                   winddir_avg2m,
                   windgustmph_10m,
                   windgustdir_10m,
               )
