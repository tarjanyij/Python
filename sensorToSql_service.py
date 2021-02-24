#!/usr/bin/python3

import os
import sys
from time import sleep
from w1thermsensor import W1ThermSensor

from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Index
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

def ds18b20_read_sensor():
    data ={}
    for sensor in W1ThermSensor.get_available_sensors():
        #print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
        data.update({sensor.id : sensor.get_temperature()})
    
    return data

if __name__ == '__main__':
    db_url = {'drivername': 'mysql+pymysql',
               'username': 'tempwriter',
               'password': 'Titok12345',
               'host': 'localhost',
               'database': 'home',
               'port': 3306 }

    engine = create_engine(URL(**db_url))

    #engine = create_engine("PyMySQL://tempwriter:Titok12345@localhost/home")
    # db_url = 'sqlite:///sqlite3.db'
    # engine = create_engine(db_url)
    Base = declarative_base()
    
    class Temperature(Base):
        __tablename__ = 'temperature'
        id = Column(Integer, primary_key=True)
        thermosensor_id = Column(String(50), ForeignKey('sensor_config.sensorid'))
        temperature = Column(Float)
        date = Column(DateTime, default=datetime.utcnow)
        SensorConfig = relationship("SensorConfig", cascade="save-update")        
    
    class SensorConfig(Base):
        __tablename__ = "sensor_config"
        id = Column(Integer, primary_key=True)
        sensorname = Column(String(50))
        sensorid = Column(String(50),index=True)

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

        except IntegrityError as e: # foreign key hiba elkapása
            session.close() # előző session lezárása
            if "a foreign key constraint fails" in str(e): #ha szerepel a hibaüziben
                x=str(e).find("'thermosensor_id':") # a string kikeresése
                sensor_id = str(e)[x+20:x+32] # a hányzó sensorid kikeres
                #print(sensor_id)
                row=SensorConfig(sensorname='', sensorid=sensor_id) # a sensorkonfig táblába írása
                session.add(row)
                session.commit()
            session.close()


        except SQLAlchemyError as e:
            session.close()
            print(e)
        except KeyboardInterrupt:
            session.close()
            print(" ")
            print("Bye")
        sleep(30)

    
