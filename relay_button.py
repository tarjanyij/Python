import os
import sys
import time

from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep


relay1 = port.PA12
relay2 = port.PA11
button = port.PA13

gpio.init()
gpio.setcfg(relay1,gpio.OUTPUT)
gpio.setcfg(relay2,gpio.OUTPUT)
gpio.setcfg(button,gpio.INPUT)


gpio.output(relay1,1)
gpio.output(relay2,1)

perv_button = True

try:
    print ("Press CTR+C to Exit")
    while True:
        input = gpio.input(button)
        if (input == 0):
            
            print("gomb lenyomva")
            if (perv_button):
                gpio.output(relay1,0)
                perv_button = False
            else:
                gpio.output(relay1,1)
                perv_button = True
        sleep(0.5)
except KeyboardInterrupt:
    print("Bye")
    gpio.output(relay1,1)
    gpio.output(relay2,1)
