# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import gc
gc.collect()

import network
ap = network.WLAN(network.AP_IF) # create access-point interface
ap.active(True) # activate the interface
ap.config(essid='physcomp-A')


import webrepl
webrepl.start()
