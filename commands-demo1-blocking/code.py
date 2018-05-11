import time
import sys
import touchio
import board

touch_a1 = touchio.TouchIn(board.A1)

def command_TOUCH1():
    v = touch_a1.raw_value
    print("%d" % (v,))

commands = {
  'TOUCH1': command_TOUCH1,
}

t0 = time.monotonic()
while True:
    t1 = time.monotonic()
    s = sys.stdin.readline()
    try:
        com_func = commands[s.strip()]
        com_func()
    except KeyError:
        print("# ERROR: INVALID COMMAND '%s'" % (s,))
