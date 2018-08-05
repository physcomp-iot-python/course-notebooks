import time
import board
import sys
import gc

import adafruit_io

import busio  #must import ahead of adafruit_vl53l0x
import adafruit_vl53l0x



# Network 'Hotspot' settings
ESSID    = 'nasa'#'Ellipsis Jetpack 1C7B'
PASSWORD = 'mars-adventure'#'f8ff0351'

#-Adafruit IO settings
USER_NAME = "nporter1" #PLEASE CHANGE TO YOUR AIO USERNAME
AIO_KEY = '05df2749793c4d67866c8e5fac57612e'  #PLEASE CHANGE TO YOUR AIO KEY

# create one adafruit_io.Feed object per sensor, configure once during
# instantiation, and use to post values many times.
# Each sensor's' feed should have a unique name!

LIDAR_FEED_NAME = 'wherewedroppinbois' #PLEASE CHANGE TO YOUR AIO FEED NAME
lidar_feed = adafruit_io.Feed(user_name = USER_NAME,
                              key = AIO_KEY,
                              feed_name = LIDAR_FEED_NAME,
                              )
print("Feed: {}".format(LIDAR_FEED_NAME))
print("headers: {}".format(lidar_feed.headers))
print("post_url: {}".format(lidar_feed.post_url))


# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
dist_sensor = adafruit_vl53l0x.VL53L0X(i2c)

def blink(sleeptime):
    import machine
    led = machine.Pin(0,machine.Pin.OUT)
    led.value(0)
    time.sleep(sleeptime)
    led.value(1)

def do_connect(essid=ESSID,password=PASSWORD):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(essid, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

################################################################################
# Main
################################################################################
#wait for 5 seconds so that ampy get get started if needed
#time.sleep(5.0)

do_connect() #connect to network

while True:
    gc.collect()
    try:
        time.sleep(0.1)
        #humid, temp = get_ht()
        #print("humid: %0.3f" % humid)
        #print("temp: %0.3f" % temp)
        range_mm = dist_sensor.range
        print(range_mm)
        if range_mm <= 1000:
            #plug into you feeds
            lidar_feed.post(range_mm)
            blink(0.5)
    except KeyboardInterrupt:
        # this is needed for ampy and other REPL interactions to work with this
        # generic error handler
        raise KeyboardInterrupt
    except Exception as exc:
        print("Caught: {}".format(repr(exc)))
        blink(5.0)
