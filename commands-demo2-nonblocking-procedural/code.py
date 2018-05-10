import time
import sys
import physcomp
import digitalio
import board

blink_delay = 1.0

led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

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

commands = { 
    'BLINK': command_BLINK,
}

time0 = time.monotonic()
buff = []
while True:
    #handle incoming commands
    num_rx = physcomp.get_usb_rx_count()
    if num_rx > 0:
        data = sys.stdin.read(num_rx)
        endl_index = data.find('\n')
        if endl_index >= 0:                   #we detected a line ending
            print("# found line ending")
            buff.append(data[:endl_index+1])  #merge last of data 
            line = "".join(buff)              #and join the buffer
            buff = [data[endl_index+1:]]      #put remainder in buffer
            #now parse the line by whitespace
            args = line.strip().split()
            print("# args=%r"%args)
            #first arg is the command name, rest get passed in
            name = args[0]
            try:
                cmd = commands[name]
                print("# calling func: %r " % cmd)
                cmd(args[1:])
            except KeyError:
                print("#ERROR: Invalid command: %s" % name)
        else:
            buff.append(data)               #save the data so far
        print("# %d bytes received: %r" % (num_rx,buff))
    #handle the blinking
    time1 = time.monotonic()
    if time1 - time0 > blink_delay:
        led.value = not led.value
        time0 = time1
    time.sleep(0.01)