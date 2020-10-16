#!/usr/bin/env python3
"""Basic blinking led example.
 
"""
 
import os
import sys
 
#if not os.getegid() == 0:
#sys.exit('Script must be run as root')
 
 
from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
 

 
ledp = port.PA12
leds = port.PA11
ledz = port.PA6
 
gpio.init()
gpio.setcfg(ledp, gpio.OUTPUT)
gpio.setcfg(leds, gpio.OUTPUT)
gpio.setcfg(ledz, gpio.OUTPUT)
 
gpio.output(ledp, 0)
gpio.output(leds, 0)
gpio.output(ledz, 0)

try:
    print ("Press CTRL+C to exit")
    while True:
        gpio.output(ledp, 1)
        sleep(3)
        gpio.output(leds, 1)
        sleep(1)
 
        gpio.output(ledp, 0)
        gpio.output(leds, 0)
        sleep(0.6)
 
        gpio.output(ledz, 1)
        sleep(3)
        gpio.output(ledz, 0)
        gpio.output(leds, 1)
        sleep(1)

        gpio.output(leds, 0)
        sleep(1)
        gpio.output(ledp, 1)
 
except KeyboardInterrupt:
    gpio.output(ledp, 0)
    gpio.output(leds, 0)
    gpio.output(ledz, 0)
    print ("Goodbye.")