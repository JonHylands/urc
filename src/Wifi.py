
import network
from binascii import hexlify


class URCAccessPoint:

    AP = "URC_WLAN"
    PWD = "roundURC_128"

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        while self.wlan.active() == False:
            pass

        print(self.wlan.ifconfig())
        print('MAC Address:')
        print(self.wlan.config('mac'))
        print(hexlify(self.wlan.config('mac'),':').decode())

URCAccessPoint()
