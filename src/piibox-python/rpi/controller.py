import os
import bottle
import sys
import socket
import time # if only I could
import pifacedigitalio as pfio
from pifacedigitalio import NoPiFaceDigitalError
import math

from datetime import datetime

from bottle import (route, run, view, error,
                    static_file, post, request,
                    default_app,redirect, abort, Bottle)
                    
# import stuff to handle Web sockets to send currents and temps  
from gevent import monkey; monkey.patch_all()                  
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.exceptions import WebSocketError
import json # use json to encode data sent via websocket

import random as r

#default_app.push()

app = Bottle()

# Set up path to views
cwd = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(cwd,'views'))

# Define the path to the static files
static = os.path.join(cwd,'static')


# set up house to default to auto_mode
auto_mode = True
tStep=0

states=[["DownHeat","Bed1Light","DiningLight","KitchenLight","HotWater"],
         ["HotWater","Bed1Light"],
         ["DiningLight","KitchenLight"],
         [],
         ["DownHeat"],
         [],
         [],
         ["UpHeat"],
         ["DownHeat","LivingLight","DiningLight","KitchenLight"],
         [],
         ["Bed2Light","Bed3Light"],
         ["DownHeat","LivingLight","Bed1Light","Bed2Light","Bed3Light","BathroomLight"],
         ["Bed1Light","BathroomLight"]]

# logfile
logfile = os.path.join(cwd,'..','..','..','logs','log.txt')

# initialise the PiFace digital I/O boards used for output control
pfio.init()

# simple wrapper for digital read and write of piface outputs
class localLEDwrapper(object):
    """An LED on the RaspberryPi"""
    def __init__(self, led_number, board):
        if led_number < 0 or led_number > 7:
            raise LEDRangeError(
                    "Specified LED index (%d) out of range." % led_number)
        else:
            if not board:
                board = 0
            self.led = led_number
            self.board = board

    def turn_on(self):
        try:
            pfio.digital_write(self.led,1,self.board)
        except NoPiFaceDigitalError:
            pass

    def turn_off(self):
        try:
            pfio.digital_write(self.led,0,self.board)
        except NoPiFaceDigitalError:
            pass

    def toggle(self):
        if self.current() == 0:
            self.turn_on()
        else:
            self.turn_off()

    def current(self):
        try:
            retval = pfio.read_output(self.led, self.board)
        except NoPiFaceDigitalError:
            retval = 0
        return retval
    
devices= {"DownHeat":localLEDwrapper(0,0),
          "UpHeat":localLEDwrapper(0,1),
          "HotWater":localLEDwrapper(1,1),
          "KitchenLight":localLEDwrapper(6,0),
          "LivingLight":localLEDwrapper(5,0),          
          "DiningLight":localLEDwrapper(7,0),
          "Cooker":localLEDwrapper(1,0),
          "Fridge":localLEDwrapper(2,0),
          "Washer":localLEDwrapper(3,0),
          "TV":localLEDwrapper(4,0),
          "BathroomLight":localLEDwrapper(5,1),
          "Bed1Light":localLEDwrapper(7,1),
          "Bed2Light":localLEDwrapper(6,1),
          "Bed3Light":localLEDwrapper(4,1)
          }

# Set up static file handler
@app.route('/static/<filepath:path>')
def static_handler(filepath):
    return static_file(filepath, root=static)

@app.route('/')
@view('home')
def home():
    UpHeatState = devices["UpHeat"].current()
    DownHeatState = devices["DownHeat"].current()
    HotWaterState = devices["HotWater"].current()
    KitchenLightState = devices["KitchenLight"].current()
    FridgeState = devices["Fridge"].current()
    CookerState = devices["Cooker"].current()
    LivingLightState = devices["LivingLight"].current()
    TVState = devices["TV"].current()
    DiningLightState = devices["DiningLight"].current()
    BathroomLightState = devices["BathroomLight"].current()
    Bed1State = devices["Bed1Light"].current()
    Bed2State = devices["Bed2Light"].current()
    Bed3State = devices["Bed3Light"].current()

    return dict(device0 = UpHeatState, device1 = DownHeatState, device2 = KitchenLightState, device3 = FridgeState,
                device4 = CookerState, device5 = LivingLightState, device6 = TVState, device7 = DiningLightState,
                device8 = BathroomLightState, device9 = Bed1State, device10 = Bed2State, device11 = Bed3State, device12 = HotWaterState,deviceAuto=auto_mode)

@app.route('/action')
@view('home')
def action():
    device = request.query.get('device', 0)
    value = int(request.query.get('value', 0))

    if device in devices:
        if value != 0:
            log('Turning device %s on' % device)
            devices[device].turn_on()
        else:
            log('Turning device %s off' % device)
            devices[device].turn_off()
    else:
        if device == "AutoMode":
            global auto_mode
            if value == 0:
                auto_mode=False
            else:
                auto_mode=True

    redirect('/')

@app.route('/camera')
@view('home')
def camera():
    return dict(device0=devices[0].current,device1=devices[1].current)

    
def log(msg):
	# log to file
	print msg
	f = open(logfile, 'a')
	f.write('%s %s\n' % (str(datetime.now()), msg))
	f.close()

@app.route('/log')
@view('log')
def viewlog():
	lines = []
	with open(logfile, 'r') as f:
		lines = f.readlines()

	return dict(lines=lines)

@app.route('/clearlog')
def viewlog():
	os.remove(logfile)
	redirect('/')

@app.route('/about')
@view('about')  
def about():
    return {}  

adc = None
# instatiate and initialise analogue to digital converter (AB electronics Delta-sigma Pi board) for inputs
try:
    from ABElectronics_DeltaSigmaPi import DeltaSigma
    adc=DeltaSigma(0x68,0x69,18) 
except IOError:
    log('No analogue to digital converter connected')


#app2=Bottle()    
@app.route('/websocket')   
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        log('Expected WebSocket request.  Got something else on /webwocket/...')
        abort(400, 'Expected WebSocket request.')

    while True:
        try:        
            if adc:
                intTemp = getTempFromVolts(adc.readVoltage(2))
                houseLoad = 12 * getCurrentFromVolts(adc.readVoltage(1))
                solarFeed = "No monitoring"
                extTemp = "Not monitored"
            else:
                intTemp = "No monitor"
                houseLoad = "No monitor"
                solarFeed = "No monitor"
                extTemp = "No monitor"

            readings = {'intTemp':intTemp, 'extTemp':extTemp, 'houseLoad':houseLoad, 'solarFeed':solarFeed}
            global tStep
            if auto_mode:
                tStep+=1
                tStep%=len(states)
                advance_state(tStep)
 
            message = json.dumps(readings)
            log("Sending data to websocket" + message)
            wsock.send(message)
            #time.sleep(1) #no point sampling too often - chip can handle up to 3.75 samples per second at full precision, we'll go for 1
            time.sleep(0.5)
        except WebSocketError:
            break


def advance_state(timeStep):
    for switch in states[timeStep]:
        devices[switch].toggle()


def getTempFromVolts(voltage):
    kelvinToCentigrade = 273
    retTemp = 0
    T0 = 25 + kelvinToCentigrade # Kelvin
    R0 = 1000 # 1kOhm at 25 deg C
    beta = 3260
    rTherm = 240 * (0.5 + (voltage/5)) / (0.5 - (voltage/5))  
    rInf = R0 * math.exp(-beta / T0)
    retTemp = beta / (math.log(rTherm / rInf))
    retTemp -= kelvinToCentigrade
    if retTemp < 5 or retTemp > 100:
        retTemp = 0 # input must be floating - we can't be near freezing!! 
    return round(retTemp,1)

def getCurrentFromVolts(voltage):
    calibrationOffset = 0.0232
    log("Raw detected voltage:" + str( voltage))
    voltage = abs(voltage) - calibrationOffset
    milliVoltsPerAmp = 10.5
    retCurrent = voltage/(milliVoltsPerAmp * 10**-3)
    if retCurrent > 30:
        retCurrent = 0 # input must be floating - max power supply is 300W ~ 30 A
    return round(retCurrent,3)

#app.mount("/websocket",app2)    

#app = default_app.pop()
server = WSGIServer(("0.0.0.0", 80), app,
                    handler_class=WebSocketHandler)
log('starting socket server %s' % server)
server.serve_forever()
log('server started to serve forever')
