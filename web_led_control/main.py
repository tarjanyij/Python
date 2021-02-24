import os
import sys

from pyA20.gpio import gpio
from pyA20.gpio import port

from flask import Flask, render_template, request , redirect

app = Flask(__name__)

ledP = port.PA12
ledS = port.PA11
ledZ = port.PA6

gpio.init()
gpio.setcfg(ledP,gpio.OUTPUT)
gpio.setcfg(ledS,gpio.OUTPUT)
gpio.setcfg(ledZ,gpio.OUTPUT)

gpio.output(ledP,0)
gpio.output(ledS,0)
gpio.output(ledZ,0)

@app.route('/')
def student():
   return render_template('form_led.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
        #result = request.form
        print (f"eredmény red:{request.form.getlist('red')}")
        print (f"eredmény yellow:{request.form.getlist('yellow')}")
        print (f"eredmény green:{request.form.getlist('green')}")     
        
        if request.form.getlist('red'):
            gpio.output(ledP,1)
            red = True
        else:
            gpio.output(ledP,0)
            red = False
        if request.form.getlist('yellow'):
            gpio.output(ledS,1)
            yellow = True
        else:
            gpio.output(ledS,0)
            yellow = False
        if request.form.getlist('green'):
            gpio.output(ledZ,1)
            green = True
        else:
            gpio.output(ledZ,0)
            green = False  
        #return redirect('/')
        return render_template("form_led.html",red=red, yellow=yellow, green=green)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000, debug = True)