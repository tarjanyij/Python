import os
import sys
import dht
import time

from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep


# initialize GPIO
DHT11_PIN = port.PA13
gpio.init()
#gpio.cleanup()

DHT11_instance = dht.DHT11(pin=DHT11_PIN)


def DHT11_print_data(DHT11_result):
    if DHT11_result.is_valid():
        print (f"Temperature: {DHT11_result.temperature}, Humidity: {DHT11_result.humidity}")
    else:
        DHT11_read_sensor()

def DHT11_read_sensor():
    DHT11_result = DHT11_instance.read()
    DHT11_print_data(DHT11_result)

if __name__ == '__main__':
    try:
        print("CTRL+C press to exit")
        while True:
            DHT11_read_sensor()
            sleep(5)
    except KeyboardInterrupt:
        print(" ")
        print("Bye")
   
    