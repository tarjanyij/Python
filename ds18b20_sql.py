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

def ds18b20_read_sensor():
    for sensor in W1ThermSensor.get_available_sensors():
        print("Sensor %s has temperature %.2f" % (sensor.id, sensor.get_temperature()))
        return sensor

if __name__ == '__main__':

    db_url = 'sqlite:///sqlite3.db'
    engine = create_engine(db_url)
    Base = declarative_base()
    
    class Temperature(Base):
        __tablename__ = 'Temperature'
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
    
    try:
        print("CTRL+C press to exit")
        while True:
            data = ds18b20_read_sensor()
            try:
                row = Temperature(thermosensor_id=data.id, temperature=data.get_temperature())
                session.add(row)
                session.commit()
            except SQLAlchemyError as e:
                print(e)
            
            sleep(5)
    except KeyboardInterrupt:
        session.close()
        print(" ")
        print("Bye")

    
