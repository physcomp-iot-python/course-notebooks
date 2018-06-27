import urequests
import board
import digitalio
import machine
import time

ESSID = 'nasa'
PASSWORD = 'mars-adventure'
FEED_NAME = 'analog-feed-test-number-1'
FEED_KEY = '3515b3ecee734780927d7f4ab1654917'
PARAMETER_PATH = 'params.txt'

headers={'Content-Type': 'application/json','X-AIO-Key':FEED_KEY}
url='https://io.adafruit.com/api/v2/donblair/feeds/'+FEED_NAME+'/data.json'

import board
from analogio import AnalogIn

def get_params():
    f=open(PARAMETER_PATH)
    p=f.read().strip().split(',')
    return p

def get_adc():
    with AnalogIn(board.ADC) as ai:
        return ai.value/65535.0
    #import machine
    #adc=machine.ADC(0)
    #return adc.read()
    
def blink(sleeptime):
    import machine
    led = machine.Pin(0,machine.Pin.OUT)
    led.value(0)
    time.sleep(sleeptime)
    led.value(1)

def post(value):
    json=dict(value=value)
    post_json(json)
    
def post_json(json):
    r=urequests.post(url,json=json,headers=headers) 
    blink(0.1)    
    return r

def do_connect(ESSID,PASSWORD):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ESSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
#json=dict(foo='0.2')
#do_connect(ESSID,PASSWORD)
#post(json)

