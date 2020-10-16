import os
import sys
from time import sleep
from w1thermsensor import W1ThermSensor

def ds18b20_read_sensor():
    for sensor in W1ThermSensor.get_available_sensors():
        print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))

if __name__ == '__main__':
    try:
        print("CTRL+C press to exit")
        while True:
            ds18b20_read_sensor()
            sleep(5)
    except KeyboardInterrupt:
        print(" ")
        print("Bye")