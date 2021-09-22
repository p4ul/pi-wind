import sys
import time

import requests
import serial
import os
from dotenv import dotenv_values

from settings import time_between_updates, debug_local
from wind_stats import WindStats

config = dotenv_values("/home/pi/pi-wind/.env")

print(config['STATION_ID'])
print(config['STATION_KEY'])

ms_to_mph = 2.237

os.system("echo 18 > /sys/class/gpio/export")
os.system("echo out > /sys/class/gpio/gpio18/direction")
ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, bytesize=8, stopbits=1, timeout=1)
last_time = time.time()


def read_from_aneometer():
    os.system("echo 1 > /sys/class/gpio/gpio18/value")
    time.sleep(0.01)
    ser.write(bytearray(b'\x04\x03\x00\x00\x00\x02\xC4\x5E'))
    time.sleep(0.01)
    os.system("echo 0 > /sys/class/gpio/gpio18/value")
    time.sleep(1)
    count = ser.inWaiting()

    retry_limit = 10
    while 1:
        if count != 0:
            anemometer_response = ser.readline()

            raw_direction = anemometer_response[5:7]
            raw_speed = anemometer_response[3:5]
            break
        elif retry_limit < 1:
            break
        else:
            retry_limit = retry_limit - 1
            time.sleep(0.250)

    try:
        direction = int.from_bytes(raw_direction, byteorder='big') / 100
        speed_ms = int.from_bytes(raw_speed, byteorder='big') / 100

        if debug_local:
            print(str(anemometer_response), str(raw_direction), str(raw_speed), "direction", str(direction), "speed",
                  str(speed_ms))
    except NameError:
        speed_ms = -1
        direction = -1

    return speed_ms, direction


windStats = WindStats()
last_upload_time = time.time() - time_between_updates
while 1:
    try:
        now_time = time.time()

        if (now_time - last_time) >= 5:
            last_time = now_time
            current_speed_ms, current_direction = read_from_aneometer()

            windStats.add_wind_reading(now_time, current_speed_ms * ms_to_mph, current_direction)

            if (now_time - last_upload_time) >= time_between_updates:
                last_upload_time = time.time()
                # create a string to hold the first part of the URL
                WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"

                WUcreds = "ID=" + config['STATION_ID'] + "&PASSWORD=" + config['STATION_KEY']
                date_str = "&dateutc=now"

                if debug_local:
                    print("debug / not uploading!" + windStats.to_get_variables())

                else:
                    r = requests.get(
                        WUurl +
                        WUcreds +
                        date_str +
                        windStats.to_get_variables() +
                        "&action=updateraw"
                    )
                    print("uploaded:" + str(r.status_code))

    except:
        print("Unexpected error:", sys.exc_info()[0])
        # raise
