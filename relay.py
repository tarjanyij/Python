import os
import sys
import time

from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep


relay1 = port.PA12
relay2 = port.PA11

gpio.init()
gpio.setcfg(relay1,gpio.OUTPUT)
gpio.setcfg(relay2,gpio.OUTPUT)

gpio.output(relay1,1)
gpio.output(relay2,1)

sleep(10)

gpio.output(relay1,0)
gpio.output(relay2,0)

sleep(10)
gpio.output(relay1,1)
gpio.output(relay2,1)