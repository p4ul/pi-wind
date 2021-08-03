#pi-wind

Sends wind speed and direction data to weatherunderground from 
a raspberry pi hooked up to a KM53B88 Anemometer, uses the MODBUS-RTU protocol
via a RS485 shield attached to a RaspberryPi 3.

## Setup
Add a `.env` file containing
```
STATION_ID=<your id>
STATION_KEY=<your key>
```


## Equipment:
- battery (9 ~ 24 volt)
- power supply for Pi
- RaspberryPi 3
- khla/sonbest KM53B88 Anemometer http://www.sonbus.com/english/products/detail/KM53B88.html
- seedstudio RS-485-Shield https://www.seeedstudio.com/RS-485-Shield-for-Raspberry-Pi.html

Also a weatherunderground account.



## Troubleshooting

1. Receive nothing back from the KM53B88 Anemometer - make sure you have the correct unit id. Mine was set to 4 when the docs said it should be 1 from the factory.
2. I was unable to get PyModbus or Minimal modbus to work with the rs485 hat.

## Reference docs

### weatherunderground reference
https://support.weather.com/s/weather-underground?language=en_US&subcategory=Personal_Weather_Stations&type=wu

