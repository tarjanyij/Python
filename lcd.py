import os
import sys
import time

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
 
  while True:
 
    # Send some test
    lcd_string("Hello",LCD_LINE_1)
    lcd_string("Joci",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("Kerlek ne legyel",LCD_LINE_1)
    lcd_string("Ideges es hangos",LCD_LINE_2)
 
    time.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("Meglatod hogy",LCD_LINE_1)
    lcd_string("ramegy az ",LCD_LINE_2)
 
    time.sleep(3)
 
    # Send some text
    lcd_string("egeszseged",LCD_LINE_1)
    lcd_string("Legy jo!!!",LCD_LINE_2)
 
    time.sleep(3)
 
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
    lcd_string("Goodbye!",LCD_LINE_1)
    gpio.cleanup()
