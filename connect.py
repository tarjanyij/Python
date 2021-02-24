from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

# db_url = {'drivername': 'postgres',
#           'username': 'postgres',
#           'password': 'postgres',
#           'host': '192.168.99.100',
#           'port': 5432}

#engine = create_engine(URL(**db_url))

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

data = {'a': 55.66, 'b': 95.27, 'c': 18.3}
try:
    for _key, _val in data.items():
        row = Temperature(thermosensor_id=_key, temperature=_val)
        session.add(row)
    session.commit()
except SQLAlchemyError as e:
    print(e)
finally:
    session.close()
