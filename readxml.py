import os
import sys
import mysql.connector
import xml.etree.ElementTree as ET

tree = ET.parse('sqlConfig.xml')
root = tree.getroot()

mydb = mysql.connector.connect(
    host=root[0].text,
    user=root[1].text,
    password=root[2].text,
    database=root[3].text
)    

mycursor = mydb.cursor()
mycursor.execute("SELECT sensor_config.sensorname, temperature \
      FROM temperature \
      INNER JOIN sensor_config \
      ON temperature.thermosensor_id=sensor_config.sensorid \
      WHERE date = (SELECT MAX(date) FROM temperature);")

myresult = mycursor.fetchall()

print(myresult)