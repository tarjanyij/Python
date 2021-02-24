import os
import sys
from time import sleep
from w1thermsensor import W1ThermSensor

def ds18b20_read_sensor():
    data ={}
    
    for sensor in W1ThermSensor.get_available_sensors():
        #print("sor: %s Sensor %s has temperature %.2f" % (i,sensor.id, sensor.get_temperature()))
        data.update({sensor.id : sensor.get_temperature()})
        
    return data

if __name__ == '__main__':
    try:
        print("CTRL+C press to exit")
        while True:
            #ds18b20_read_sensor()
           
            data = ds18b20_read_sensor()
            #print (data)
            for sensorid, temp in data.items():
                print ("Sensor {} has temperature {}".format(sensorid, temp))
            
            sleep(5)
    except KeyboardInterrupt:
        print(" ")
        print("Bye")