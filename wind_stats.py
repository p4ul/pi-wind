class WindStats:
    __winddir = 0.0  # [0 - 360 instantaneous wind direction]
    __windspeedmph = 0.0  # [mph instantaneous wind speed]
    __windgustmph = 0.0  # [mph current wind gust, using software specific time period]
    __windgustdir = 0.0  # [0 - 360 using software specific time period]
    __windspdmph_avg2m = 0.0  # [mph 2 minute average wind speed mph]
    __winddir_avg2m = 0.0  # [0 - 360 2 minute average wind direction]
    __windgustmph_10m = 0.0  # [mph past 10 minutes wind gust mph]
    __windgustdir_10m = 0.0  # [0 - 360 past 10 minutes wind gust direction]

    def add_wind_reading(self, current_time, speedmph, direction):
        self.__winddir = direction
        self.__windspeedmph = speedmph

    def to_get_variables(self):
        return "&winddir=%.1f" \
               "&windspeedmph=%.1f" \
               "&windgustmph=%.1f" \
               "&windgustdir=%.1f" \
               "&windspdmph_avg2m=%.1f" \
               "&winddir_avg2m=%.1f" \
               "&windgustmph_10m=%.1f" \
               "&windgustdir_10m=%.1f" % (
                   self.__winddir,
                   self.__windspeedmph,
                   self.__windgustmph,
                   self.__windgustdir,
                   self.__windspdmph_avg2m,
                   self.__winddir_avg2m,
                   self.__windgustmph_10m,
                   self.__windgustdir_10m,
               )
