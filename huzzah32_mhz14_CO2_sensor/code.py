import utime
from mhz14 import MHZ14

co2_sensor = MHZ14()
co2_sensor.init()

data = {}
while True:
    try:
        co2_sensor.get_data(data)
        print(data['co2_ppm'])   
        utime.sleep(2.0)
    except Exception as err:
        print("Caught exception: {}".format(repr(err)))