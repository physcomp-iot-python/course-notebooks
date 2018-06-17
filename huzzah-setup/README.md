# physcomp-sprint-001

## flashing the firmware

https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

esptool.py --port /dev/ttyUSB0 erase_flash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 firmware.bin

## configuring the webrepl

https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl

##

https://medium.com/@JockDaRock/micropython-esp8266-quick-start-part-4-connect-to-wifi-router-7329076ee330

192.168.43.113

