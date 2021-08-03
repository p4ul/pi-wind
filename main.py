import time

import requests
import serial
import os
from dotenv import dotenv_values

config = dotenv_values(".env")

print(config['STATION_ID'])
print(config['STATION_KEY'])

os.system("echo 18 > /sys/class/gpio/export")
os.system("echo out > /sys/class/gpio/gpio18/direction")
ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, bytesize=8, stopbits=1, timeout=1)
last_time = time.time()
count = 0
while 1:
    now_time = time.time()
    if (now_time - last_time) >= 1:
        last_time = now_time
        os.system("echo 1 > /sys/class/gpio/gpio18/value")
        time.sleep(0.01)
        ser.write(bytearray(b'\x04\x03\x00\x00\x00\x02\xC4\x5E'))
        time.sleep(0.01)
        os.system("echo 0 > /sys/class/gpio/gpio18/value")
        time.sleep(1)
        count = ser.inWaiting()
        print("waiting count (this should be 9) " + str(count))

    if count != 0:
        x = ser.readline()

        rawDirection = x[5:7]
        rawSpeed = x[3:5]
        print(rawDirection)
        direction = int.from_bytes(rawDirection, byteorder='big')
        speed = int.from_bytes(rawSpeed, byteorder='big')
        print(str(x), str(rawDirection), str(rawSpeed), "direction", str(direction / 100), "speed", str(speed / 100))

        # possible things to upload
        # winddir - [0 - 360 instantaneous wind direction]
        # windspeedmph - [mph instantaneous wind speed]
        # windgustmph - [mph current wind gust, using software specific time period]
        # windgustdir - [0 - 360 using software specific time period]
        # windspdmph_avg2m - [mph 2 minute average wind speed mph]
        # winddir_avg2m - [0 - 360 2 minute average wind direction]
        # windgustmph_10m - [mph past 10 minutes wind gust mph]
        # windgustdir_10m - [0 - 360 past 10 minutes wind gust direction]

        # create a string to hold the first part of the URL
        WUurl = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?"

        WUcreds = "ID=" + config['STATION_ID'] + "&PASSWORD=" + config['STATION_KEY']
        date_str = "&dateutc=now"

        r= requests.get(
            WUurl +
            WUcreds +
            date_str +
            "&winddir=" + str(direction/100) +
            "&windspeedmph=" + str(float(speed/100) * 2.237) +
            "&action=updateraw"
        )
        print(r.url)
        print(r)
        time.sleep(10)