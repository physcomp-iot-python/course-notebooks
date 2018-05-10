################################################################################
# code.py - Blink Command Demo (Object-Oriented version)
################################################################################
#built-in modules
import time
import sys
import physcomp
import digitalio
import board

#local
from commands import CommandParser

################################################################################
# GLOBALS

blink_delay = 1.0

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

touch_inputs = {}

################################################################################
# COMMANDS

def command_TOUCH(context):
    global blink_delay
    if context.nargs == 0:
        raise TypeError("%s takes 1 argument (%d given)" % (context.name,context.nargs))
    elif context.nargs == 1:
        num = int(context.argv[0])
        #look in local sensor cache
        touch = touch_inputs.get(num)
        if touch is None: #not in cache, so initialize
            #dynamically get `board.An` attribute
            pin = getattr(board,'A%d' % num)                  #could raise exception AttributeError
            touch_inputs[num] = touch = touchio.TouchIn(pin)  #save in cache for next time
        val = touch.raw_value
        context.print("%d" % val) #send value back
    else:
        raise TypeError("%s takes 1 argument (%d given)" % (context.name,context.nargs))

def command_BLINK(context):
    global blink_delay
    if context.nargs == 0:
        blink_delay = 1.0
    elif context.nargs == 1:
        blink_delay = float(context.argv[0])
    else:
        raise TypeError("%s takes up to 1 argument (%d given)" % (context.name,context.nargs))
    context.print("# set blink_delay=%f" % blink_delay)
    
CP = CommandParser()
CP.attach("TOUCH", command_TOUCH)
CP.attach("BLINK", command_BLINK)

################################################################################
# MAIN LOOP

time0 = time.monotonic()
while True:
    #handle incoming commands
    num_rx = physcomp.get_usb_rx_count()
    if num_rx > 0:
        data = sys.stdin.read(num_rx)
        CP.feed(data)
    #handle the blinking
    time1 = time.monotonic()
    if time1 - time0 > blink_delay:
        led.value = not led.value
        time0 = time1
    time.sleep(0.01)
