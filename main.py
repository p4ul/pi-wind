import time
import serial
import os
send_str = "********abcdefghijklmnopqrstuvwxyz&"
os.system("echo 18 > /sys/class/gpio/export")
os.system("echo out > /sys/class/gpio/gpio18/direction")
ser = serial.Serial(port='/dev/ttyS0',baudrate=9600,bytesize=8,stopbits=1,timeout=1)
last_time = time.time()
count = 0
while 1:
     now_time = time.time()
     if((now_time-last_time)>=1):
        last_time = now_time
        print("172 sending")
        os.system("echo 1 > /sys/class/gpio/gpio18/value")
        time.sleep(0.01)
        ser.write(bytearray(b'\x04\x03\x00\x00\x00\x02\xC4\x5E'))
        time.sleep(0.01)
        os.system("echo 0 > /sys/class/gpio/gpio18/value")
        #os.system("echo 0 > /sys/class/gpio/gpio18/value")
        time.sleep(0.01)
        count = ser.inWaiting()
     if(count != 0):
        x=ser.readline()
        # if "********" in x:
        # print "str length is: " + str(count)
        print (x)

