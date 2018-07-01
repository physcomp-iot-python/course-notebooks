################################################################################
# mhz14.py
#
#  Driver for Winsen MHZ-14 or MHZ-19- NDIR CO2 SENSOR.
#  Based off of code for ESP8266 using custom SoftUART firmware:
#  https://github.com/p-v-o-s/mycopython/blob/master/mhz14.py
#  https://github.com/p-v-o-s/micropython
#  This code has been updated to work with hardware UART on standard
#  micropython releases for the ESP32 SoC
#
#  author: Craig Versek (cversek@gmail.com)
#  license: 
################################################################################
import utime
import machine

DEBUG = False
#DEBUG = True


CMD_REQUEST_PPM          = bytes((0xFF,0x01,0x86,0x00,0x00,0x00,0x00,0x00,0x79))
CMD_CALIBRATE_ZERO_POINT = bytes((0xFF,0x01,0x87,0x00,0x00,0x00,0x00,0x00,0x78))

#note that byte i=3 must be set to the "high byte" reading and byte i=4 set to
#the "low byte" reading for the maximum concentration range AND byte i=8
#should be computed as the checksum = (~sum(b[1:8]) + 1) & 0xFF
CMD_CALIBRATE_SPAN_POINT = bytearray((0xFF,0x01,0x88,0x00,0x00,0x00,0x00,0x00,0x00))

class MHZ14(object):
    """driver for Winsen MHZ-14 - NDIR CO2 SENSOR
       http://www.winsen-sensor.com/products/ndir-co2-sensor/mh-z14.html
    """
    def __init__(self, uart_num = 1, tx = 17, rx = 16):
        self._ser = machine.UART(uart_num, baudrate=9600, tx=tx, rx=rx)
        self._data_buff = bytearray(9)
        self.active = False
        
    def init(self):
        self._wakeup()
        
    def _wakeup(self):
        #sensor can inititally be in a weird state, so talk to it twice and then flush
        self._ser.write(CMD_REQUEST_PPM)
        utime.sleep_ms(1000)
        #m.geself._ser.flush()
        for i in range(5):
            self._ser.write(CMD_REQUEST_PPM)
            utime.sleep_ms(10)
            self._ser.readinto(self._data_buff)
            if self._data_buff[0] == 0xFF: #possibly valid data
                db = self._data_buff
                #compute checksum to validate data
                checksum = ~sum(db[1:8])+1 & 0xFF
                if DEBUG:
                    print(db,checksum)
                if checksum == db[8]: #data is valid, so we are ready
                    self.active = True
                    break
            #repeat until we get valid data
            utime.sleep_ms(1000)
        else:
            print("WARNING: Initialization of MH-Z14 sensor failed!\n\tsetting attribute active=False")
            self.active = False
        
    def get_data(self, d = None, timeout = 2):
        if d is None:
            d = {}
        if not self.active:
            return d
        else:
            #self._ser.flush()
            self._ser.write(CMD_REQUEST_PPM)
            start_time = utime.ticks_ms()
            while True:
                if utime.ticks_ms() - start_time > timeout*1000:
                    raise Exception("data request timed out")
                utime.sleep_ms(10)
                self._ser.readinto(self._data_buff)
                if DEBUG:
                    print(self._data_buff)
                if self._data_buff[0] == 0xFF: #possibly valid data
                    break
            db = self._data_buff
            #compute checksum to validate data
            checksum = ~sum(db[1:8])+1 & 0xFF
            if DEBUG:
                print(db,checksum)
            if checksum != db[8]:
                print("WARNING: AM2315 sensor sent repsonse with a bad checksum!")
                d['co2_ppm'] = float('nan')
            else:
                d['co2_ppm'] = (256*db[2] + db[3])
            return d
        
    def calibrate_zero_point(self):
        self._ser.write(CMD_REQUEST_PPM)
        
################################################################################
# TEST CODE
################################################################################
if __name__ == "__main__":
    mhz = MHZ14()
    d = {}
    mhz.get_data(d)
    print(d)
