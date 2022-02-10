# ENGD3000 - Final Year Project - 2020/2021
# Supervisor: Richard Snape
# Student: Henrik Nyby

# Import libraries
import os
import bottle
import sys
import socket
import time # To be used in future updates
import math

# Import PiFace Digital IO libraries
import pifacedigitalio as pfio
from pifacedigitalio import NoPiFaceDigitalError

from datetime import datetime
from bottle import (route, run, view, error,
                    static_file, post, request,
                    default_app,redirect, abort, Bottle)

# Import stuff to handle Web sockets to send currents and temperatures
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.exceptions import WebSocketError
import json # Use json to encode data sent via websocket
import random as r

# Debug scaffolding code
TRACE = 1
DEBUG = 2
WARNING = 3
ERROR = 4
NON = 5
debug_level = DEBUG    # Set debug level

# Default_app.push()
app = Bottle()

# Set up path to views (current working directory)
cwd = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(cwd,'views'))

# Set up path to static files
static = os.path.join(cwd,'static')

# Set energy mode to auto_mode
# Improvements here EnergyMode class/object
# EnergyMode(1) -> auto_mode
# EnergyMode(2) -> co2_mode
# EnergyMode(3) -> pv_mode
# EnergyMode(4) -> low_tarif_modef
# EnergyMode(5) -> grid_mode

# Initialise auto mode
auto_mode = True
all_off = True
tStep=0

# Define auto_mode sequential schedule
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
         ["Bed1Light","Bed2Light","Bed3Light"],
         ["DownHeat","LivingLight","Bed1Light","Bed2Light","Bed3Light","BathroomLight"],
         ["Bed1Light","BathroomLight"]]

# Set path to the log file
logfile = os.path.join(cwd,'..','..','..','logs','log.txt')

# Initialise PiFace digital I/O hardware on top (HAT)
pfio.init()

## NOTE TO HENRIK : RICHARD ADDED 2021_03_19 @ 19:45 to fix the state reading
boards = [pfio.PiFaceDigital(0),pfio.PiFaceDigital(1)]
#boards = [pfio.PiFaceDigital(0),pfio.PiFaceDigital(1),pfio.PiFaceDigital(2)]

# Simple wrapper (object) for digital read and write of piface outputs
class localLEDwrapper(object):
    """An LED on the RaspberryPi"""
    def __init__(self, led_number, board):
        if led_number < 0 or led_number > 7:
            if debug_level<=ERROR:
                log("Specified LED index (%d) out of range." %led_number)
            raise LEDRangeError(
                    "Specified LED index (%d) out of range." % led_number)
        else:
            if not board:
                board = 0
            self.led = led_number
            self.board = board
            self.board_object = boards[board] ## NOTE TO HENRIK : RICHARD ADDED 2021_03_19 @ 19:45 to fix the state reading

    def turn_on(self):
        try:
            pfio.digital_write(self.led,1,self.board)
        except NoPiFaceDigitalError:
            if debug_level<= ERROR:
                log('Big trouble!!!! No pifacedigital to write to:(')

    def turn_off(self):
        try:
            pfio.digital_write(self.led,0,self.board)
        except NoPiFaceDigitalError:
            if debug_level<=ERROR:
                log('Big trouble!!!! No pifacedigital to write to:(')

    def toggle(self):
        if self.current() == 0:
            self.turn_on()
        else:
            self.turn_off()

    def current(self):
        try:
            ## NOTE TO HENRIK : RICHARD ADDED 2021_03_19 @ 19:45 to fix the state reading
            retval = self.board_object.output_pins[self.led].value
        except NoPiFaceDigitalError:
            if debug_level<=ERROR:
                log('Big trouble!!!! No pifacedigital to read:( returning default')
            retval = 0
        return retval

# Define all home devices, (improvements to be made, modular coding)
devices= {"DownHeat":localLEDwrapper(0,0),
          "Cooker":localLEDwrapper(1,0),
          "Fridge":localLEDwrapper(2,0),
          "Washer":localLEDwrapper(3,0),
          "TV":localLEDwrapper(4,0),
          "LivingLight":localLEDwrapper(5,0),
          "KitchenLight":localLEDwrapper(6,0),
          "DiningLight":localLEDwrapper(7,0),
          "UpHeat":localLEDwrapper(0,1),
          "HotWater":localLEDwrapper(1,1),
          "BatteryStorage": localLEDwrapper(2,1),
          "SolarPV": localLEDwrapper(3,1),
          "Bed3Light":localLEDwrapper(4,1),
          "BathroomLight":localLEDwrapper(5,1),
          "Bed2Light":localLEDwrapper(6,1),
          "Bed1Light":localLEDwrapper(7,1),
          #"AdditionalOutput0": localLEDwrapper(0,2),	#KitchenKetttle
          #"AdditionalOutput1": localLEDwrapper(1,2),	#KitchenFreezer
          #"AdditionalOutput2": localLEDwrapper(2,2),   #KitchenPowerPoint
          #"AdditionalOutput3": localLEDwrapper(3,2),   #BedroomPowerPoint
          #"AdditionalOutput4": localLEDwrapper(4,2),	#LivingRoomPowerPoint
          #"AdditionalOutput5": localLEDwrapper(5,2),	#DinningPowerPoint
          #"AdditionalOutput6": localLEDwrapper(6,2),	#GardenLight
          #"AdditionalOutput7": localLEDwrapper(7,2)	#GardenSprinkler
          }

# Set up static file handler
@app.route('/static/<filepath:path>')
def static_handler(filepath):
    return static_file(filepath, root=static)

# Define webserver homepage
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
    SolarPVState = devices["SolarPV"].current()
    BatteryState = devices["BatteryStorage"].current()
    #AddOut0State = devices["AdditionalOutput0"].current()
    #AddOut1State = devices["AdditionalOutput1"].current()
    #AddOut2State = devices["AdditionalOutput2"].current()
    #AddOut3State = devices["AdditionalOutput3"].current()
    #AddOut4State = devices["AdditionalOutput4"].current()
    #AddOut5State = devices["AdditionalOutput5"].current()
    #AddOut6State = devices["AdditionalOutput6"].current()
    #AddOut7State = devices["AdditionalOutput7"].current()

    return dict(device0 = UpHeatState, device1 = DownHeatState, device2 = KitchenLightState, device3 = FridgeState,
                device4 = CookerState, device5 = LivingLightState, device6 = TVState, device7 = DiningLightState,
                device8 = BathroomLightState, device9 = Bed1State, device10 = Bed2State, device11 = Bed3State,
                device12 = HotWaterState, device13 = SolarPVState, device14 = BatteryState, deviceAuto=auto_mode,
                deviceAllOff=all_off)
                #device15 = AddOutState0, device16 = AddOutState1, device17 = AddOutState2, device18 = AddOutState3)
                #device19 = AddOutState4, device20 = AddOutState5, device21 = AddOutState6, device22 = AddOutState7)

@app.route('/action')
@view('home')
def action():
    device = request.query.get('device', 0)
    value = int(request.query.get('value', 0))

    # device fetched from the webserver 
    if device in devices:
        if value != 0:
            if debug_level<=ERROR:
                log('%s ON' % device)
            devices[device].turn_on()
        else:
            if debug_level<=ERROR:
                log('%s OFF' % device)
            devices[device].turn_off()

    elif device == "AutoMode":
        global auto_mode
        if value == 0:
            auto_mode=False
        else:
            auto_mode=True
    else:
        if device == "AllOff":
            global all_off
            if value == 0:
                all_off=False
		if debug_level<=ERROR:
		    log('%s are OFF' %device)
                    for b in boards:
                        b.output_port.all_off()
                   # pfio.output_port.all.off()
  	    else:
		all_off=True
		if debug_level<=ERROR:
		    log('%s State not changed' %device)
		#pfio.output_port.all.off()

    if getTempFromVoltsTwo(adc.readVoltage(3)) >= 23:
        auto_mode=False
        if debug_level<=ERROR:
            log('TEST temperature detection')

    #new_msg=boards[1].input_pins[3].value
    #log('INPUT is %s'%new_msg)
    redirect('/')

# Define webserver camera view
@app.route('/camera')
@view('home')
def camera():
    return dict(device0=devices[0].current,device1=devices[1].current)

def log(msg):
    # log to file
    #print msg()
    f = open(logfile, 'a')
    f.write('%s %s\n' % (str(datetime.now()), msg))
    f.close()

# Define webserver log-file page
@app.route('/log')
@view('log')
def viewlog():
    lines = []
    with open(logfile, 'r') as f:
        lines = f.readlines()

    return dict(lines=lines)

# Define webserver clear log file command
@app.route('/clearlog')
def viewlog():
    os.remove(logfile)
    log('Log file cleared and restarted')
    redirect('/')    # Redirect to homepage

@app.route('/about')
@view('about')
def about():
    return {}

# Sitemap with all links
@app.route('/sitemap')
@view('sitemap')
def sitemap():
    return {}

# Test to set up a monitor page
@app.route('/dashboard')
@view('dashboard')
def dashboard():
    return{}

# Test to set up a video streat page
@app.route('/camera')
@view('camera')
def camera():
    return{}

adc = None
# Instatiate and initialise analogue to digital converter (AB electronics Delta
try:
    from ABElectronics_DeltaSigmaPi import DeltaSigma
    adc=DeltaSigma(0x68,0x69,18)
    if debug_level<=ERROR:
        log('Connected to the ADC PI Delta-Sigma')
        log('Readings at channel 1-4 : %s %s %s %s' % (adc.readVoltage(1),adc.readVoltage(2), adc.readVoltage(3), adc.readVoltage(4)))
        log('Readings at channel 5-8 : %s %s %s %s' % (adc.readVoltage(5),adc.readVoltage(6), adc.readVoltage(7), adc.readVoltage(8)))
except IOError:
    log('No ADC connected')

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
                houseLoad = 12 * getCurrentFromVolts(adc.readVoltage(1))
                intTemp = getTempFromVolts(adc.readVoltage(2))
                solarFeed = 12 * getCurrentFromVolts(adc.readVoltage(4))
                extTemp =  getTempFromVoltsTwo(adc.readVoltage(3))
                kitchenTemp =  getTempFromMilliVolts(adc.readVoltage(5))
                dinningTemp =  getTempFromMilliVolts(adc.readVoltage(6))
                bathroomTemp =  getTempFromMilliVolts(adc.readVoltage(7))
                bedroomTemp =  getTempFromMilliVolts(adc.readVoltage(8))
            else:
                intTemp = "No monitor"
                houseLoad = "No monitor"
                solarFeed = "No monitor"
                extTemp = "No monitor"
                kitchenTemp = "No monitor"
                dinningTemp = "No monitor"
                bathroomTemp = "No monitor"
                bedroomTemp = "No monitor"

            readings = {'intTemp':intTemp, 'extTemp':extTemp, 'houseLoad':houseLoad, 'solarFeed':solarFeed, 'kitchenTemp':kitchenTemp, 'dinningTemp':dinningTemp, 'bathroomTemp':bathroomTemp, 'bedroomTemp':bedroomTemp}
            global tStep
            if auto_mode:
                tStep+=1
                tStep%=len(states)
                advance_state(tStep)

            message = json.dumps(readings)
            if debug_level==TRACE:
                log("Sending data to websocket" + message)
            wsock.send(message)
            #time.sleep(1) #no point sampling too often - chip can handle up to 3.75 samples per second at full precision, we'll go for 1
            time.sleep(0.5)
        except WebSocketError:
            break


def advance_state(timeStep):
    for switch in states[timeStep]:
        devices[switch].toggle()

# Function to read temperture on first thermistor
def getTempFromVolts(voltage):
    kelvinToCentigrade = 273
    retTemp = 0
    T0 = 25 + kelvinToCentigrade # Kelvin
    R0 = 1000 # 1kOhm at 25 deg C per datasheet
    beta = 3260
    rTherm = 240 * (0.5 + (voltage/5)) / (0.5 - (voltage/5))
    rInf = R0 * math.exp(-beta / T0)
    retTemp = beta / (math.log(rTherm / rInf))
    retTemp -= kelvinToCentigrade
    if retTemp < 5 or retTemp > 100:
        retTemp = 0 # Input must be floating - we can't be near freezing!!
    return round(retTemp,1)

# Function to read temperture on second thermistor
def getTempFromVoltsTwo(voltage):
    kelvinToCentigrade = 273
    retTemp = 0
    T0 = 25 + kelvinToCentigrade # Kelvin
    R0 = 275 # 275 Ohm at 25 deg C as tested
    beta = 3260
    rTherm = 240 * (0.5 + (voltage/5)) / (0.5 - (voltage/5))
    rInf = R0 * math.exp(-beta / T0)
    retTemp = beta / (math.log(rTherm / rInf))
    retTemp -= kelvinToCentigrade
    if retTemp < 5 or retTemp > 100:
        retTemp = 0 # Input must be floating - we can't be near freezing!!
    return round(retTemp,1)

def getCurrentFromVolts(voltage):
    calibrationOffset = 0.0232
    if debug_level==DEBUG:
        log("Raw detected voltage:" + str( voltage))
    voltage = abs(voltage) - calibrationOffset
    milliVoltsPerAmp = 10.5
    retCurrent = voltage/(milliVoltsPerAmp * 10**-3)
    if retCurrent > 30:
        retCurrent = 0 # Input must be floating - max power supply is 300W ~ 30 A
    return round(retCurrent,3)

# Function to convert LM35 temprature reading to volts
# v_out = 10mV/C*T


def getTempFromMilliVolts(mVolts):
    scale_factor = 10	# Linear Scale Factor 10mV/C
    conv_to_volts = 1000
    temp = (mVolts/scale_factor)*conv_to_volts
    if debug_level==DEBUG:
        log("Raw detected milli voltage:" + str(mVolts))
    return round(temp,2)


#app.mount("/websocket",app2)
log('Loglevel is %s '%debug_level)
#app = default_app.pop()
server = WSGIServer(("0.0.0.0", 80), app,
                    handler_class=WebSocketHandler)
log('Starting socket server %s' % server)
log('Default values of current/ temp are %s %s' % (getCurrentFromVolts(0),getTempFromVolts(0)))

server.serve_forever()
log('server started to serve forever')
