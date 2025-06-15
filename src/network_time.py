
from machine import RTC
import network
import ntptime
import time

class NetworkTime:
    def __init__(self):
        self.station = network.WLAN(network.STA_IF)
        self.connect("*****", "*******")
        self.rtc = RTC()
        ntptime.settime()
        (year, month, day, weekday, hours, minutes, seconds, subseconds) = self.rtc.datetime()
        print ("UTC Time: ")
        print((year, month, day, hours, minutes, seconds))

        sec = ntptime.time()
        timezone_hour = 5.50
        timezone_sec = timezone_hour * 3600
        sec = int(sec + timezone_sec)
        (year, month, day, hours, minutes, seconds, weekday, yearday) = time.localtime(sec)
        print ("IST Time: ")
        print((year, month, day, hours, minutes, seconds))
        self.rtc.datetime((year, month, day, 0, hours, minutes, seconds, 0))
        self.disconnect()

    def connect(self, id, pswd):
        ssid = id
        password = pswd
        if self.station.isconnected() == True:
            print("Already connected")
            return
        self.station.active(True)
        self.station.connect(ssid, password)
        while self.station.isconnected() == False:
            pass
        print("Connection successful")
        print(self.station.ifconfig())

    def disconnect(self):
        if self.station.active() == True: 
            self.station.active(False)
        if self.station.isconnected() == False:
            print("Disconnected") 
 
