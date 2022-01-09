import machine
import math
import network
import os
import time
import utime
import gc
import pycom
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pycoproc_2 import Pycoproc

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08)  # white

time.sleep(2)
gc.enable()

# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print("\nRTC Set from NTP to UTC:", rtc.now())
utime.timezone(7200)
print("Adjusted from UTC to EST timezone", utime.localtime(), "\n")

py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYTRACK:
    raise Exception("Not a Pytrack")

time.sleep(1)
l76 = L76GNSS(py, timeout=30, buffer=512)

pybytes_enabled = False
if "pybytes" in globals():
    if pybytes.isconnected():
        print("Pybytes is connected, sending signals to Pybytes")
        pybytes_enabled = True


while True:
    coord = l76.coordinates()
    f.write("{} - {}\n".format(coord, rtc.now()))
    print("{} - {} - {}".format(coord, rtc.now(), gc.mem_free()))
    if pybytes_enabled:
        pybytes.send_signal(1, coord)
    
    li = LIS2HH12(py)
    print("Acceleration: " + str(li.acceleration()))
    print("Roll: " + str(li.roll()))
    print("Pitch: " + str(li.pitch()))
    time.sleep(10)
