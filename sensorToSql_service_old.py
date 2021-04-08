#!/usr/bin/python3

import os
import sys
from time import sleep
from w1thermsensor import W1ThermSensor

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import xml.etree.ElementTree as ET

def ds18b20_read_sensor():
    data ={}
    for sensor in W1ThermSensor.get_available_sensors():
        #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
        data.update({sensor.id : sensor.get_temperature()})
    
    return data

if __name__ == '__main__':
    tree = ET.parse('/home/tarjanyij/Python/sqlConfig.xml')
    root = tree.getroot()

    db_url = {'drivername': 'mysql+pymysql',
               'username': root[1].text,
               'password': root[2].text,
               'host': root[0].text,
               'database': root[3].text,
               'port': 3306 }

    engine = create_engine(URL(**db_url))
    
    Base = declarative_base()
    
    class Temperature(Base):
        __tablename__ = 'temperature'
        id = Column(Integer, primary_key=True)
        thermosensor_id = Column(String(50))
        temperature = Column(Float)
        date = Column(DateTime, default=datetime.utcnow)        
   
    # create tables
    Base.metadata.create_all(bind=engine)

    # create session
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    
    while True:
        
        data = ds18b20_read_sensor() # Átvesszük a dictionary-t 
        rowList = [] #Egy üres listát készítünk
        
        try:
            # egyesével kiolvassuk a dictionary elemeit
            for sensorid, temp in data.items():
                #teljesítmény problémák miatt nem jó dokumentáció szerint     
                ##row = Temperature(thermosensor_id=sensorid, temperature=temp)
                ##print ("termosensor id: {} temperature : {}".format(row.thermosensor_id,row.temperature))
                ##session.add(row)
                ##session.comit()

                rowList.append(Temperature(thermosensor_id=sensorid, temperature=temp)) # beletesszük listába a temperature objektum elemeit
              
            session.add_all(rowList) # a lista elemeit beirjuk az adatbázisba (ez jobb teljesítményt ad mint session.add)
            session.commit() # adadbeírás lezárása
            
        except SQLAlchemyError as e:
            session.close()
            print(e)
        
        sleep(30)

    
