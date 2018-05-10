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

################################################################################
# COMMANDS

def command_BLINK(argv):
    global blink_delay
    nargs = len(argv)
    if nargs == 0:
        blink_delay = 1.0
    elif nargs == 1:
        blink_delay = float(argv[0])
    else:
        raise TypeError("%s takes up to 1 argument (%d given)" % (__name__,nargs))
    print("# set blink_delay=%f" % blink_delay)
    
CP = CommandParser()
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
