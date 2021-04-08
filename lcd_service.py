#!/usr/bin/python3

import os
import sys
import time
import psutil
import mysql.connector
import xml.etree.ElementTree as ET

from pyA20.gpio import gpio
from pyA20.gpio import port
from time import sleep

# Define gpio to LCD mapping
LCD_RS = port.PA10
LCD_E  = port.PA20
LCD_D4 = port.PA19
LCD_D5 = port.PA7
LCD_D6 = port.PA8
LCD_D7 = port.PA9
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

# 
lcd_wait = 5

def main():
  # Main program block
  
  gpio.init()
  gpio.setcfg(LCD_E, gpio.OUTPUT)  # E
  gpio.setcfg(LCD_RS, gpio.OUTPUT) # RS
  gpio.setcfg(LCD_D4, gpio.OUTPUT) # DB4
  gpio.setcfg(LCD_D5, gpio.OUTPUT) # DB5
  gpio.setcfg(LCD_D6, gpio.OUTPUT) # DB6
  gpio.setcfg(LCD_D7, gpio.OUTPUT) # DB7
 
  # Initialise display
  lcd_init()
  
  tree = ET.parse('sqlConfig.xml')
  root = tree.getroot()

  mydb = mysql.connector.connect(
    host=root[0].text,
    user=root[1].text,
    password=root[2].text,
    database=root[3].text
  )     
  mycursor = mydb.cursor()

  while True:
 
    # Send some test
    #lcd_string("Hello",LCD_LINE_1)
    #lcd_string("Joci",LCD_LINE_2)
    #time.sleep(3) # 3 second delay

    lcd_show("H E L L O", "I am a computer" )

    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().used/(1024*1024)
    txtMem = "Mem use: {:.0f} MB"
    lcd1 = "CPU use: " + str(cpu) + "%"
    lcd2 = txtMem.format(mem)
    lcd_show(lcd1,lcd2)

    t = psutil.sensors_temperatures()
    boardTemp = t["w1_slave_temp"][1][1]
    cpuTemp = t["cpu_thermal"][0][1]
    txtCpu = "Cpu temp: {:.0f} C"
    txtBoard = "Board temp: {:.0f} C"
    lcd1 = txtCpu.format(cpuTemp)
    lcd2 = txtBoard.format(boardTemp)
    lcd_show(lcd1,lcd2)

    mycursor.execute("SELECT sensor_config.sensorname, temperature \
      FROM temperature \
      INNER JOIN sensor_config \
      ON temperature.thermosensor_id=sensor_config.sensorid \
      WHERE date = (SELECT MAX(date) FROM temperature);")
    myresult = mycursor.fetchall()
    
    for x in myresult:
      lcd1 = x[0] + " : " 
      txtTemp = "         {:.1F} C"
      lcd2 = txtTemp.format(x[1])
      lcd_show(lcd1,lcd2)
      

def lcd_show(lcd1,lcd2):
  lcd_string(lcd1,LCD_LINE_1)
  lcd_string(lcd2,LCD_LINE_2)
  time.sleep(lcd_wait)
  


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  gpio.output(LCD_RS, mode) # RS
 
  # High bits
  gpio.output(LCD_D4, False)
  gpio.output(LCD_D5, False)
  gpio.output(LCD_D6, False)
  gpio.output(LCD_D7, False)
  if bits&0x10==0x10:
    gpio.output(LCD_D4, True)
  if bits&0x20==0x20:
    gpio.output(LCD_D5, True)
  if bits&0x40==0x40:
    gpio.output(LCD_D6, True)
  if bits&0x80==0x80:
    gpio.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  gpio.output(LCD_D4, False)
  gpio.output(LCD_D5, False)
  gpio.output(LCD_D6, False)
  gpio.output(LCD_D7, False)
  if bits&0x01==0x01:
    gpio.output(LCD_D4, True)
  if bits&0x02==0x02:
    gpio.output(LCD_D5, True)
  if bits&0x04==0x04:
    gpio.output(LCD_D6, True)
  if bits&0x08==0x08:
    gpio.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  gpio.output(LCD_E, True)
  time.sleep(E_PULSE)
  gpio.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    #lcd_string("Goodbye!",LCD_LINE_1)
    #gpio.cleanup()
