import os
import bottle
import sys
import socket
import piface.pfio as pfio
import cv2
import base64
from datetime import datetime

from bottle import (route, run, view, error,
                    static_file, post, request,
                    default_app,redirect)

default_app.push()

# Set up path to views
cwd = os.path.dirname(__file__)
bottle.TEMPLATE_PATH.append(os.path.join(cwd,'views'))

# Define the path to the static files
static = os.path.join(cwd,'static')

# logfile
logfile = os.path.join(cwd,'..','..','..','logs','log.txt')

pfio.init()
devices= {0:pfio.LED(0),1:pfio.LED(1)}

# Set up static file handler
@route('/static/<filepath:path>')
def static_handler(filepath):
    return static_file(filepath, root=static)

@route('/')
@view('home')
def home():
    device0 = devices[0].current
    device1 = devices[1].current
    return dict(device0 = device0, device1 = device1)

@route('/action')
@view('home')
def action():
    device = int(request.query.get('device', 0))
    value = int(request.query.get('value', 0))

    if value != 0:
        log('Turning device %s on' % device)
        devices[device].turn_on()
    else:
        log('Turning device %s off' % device)
        devices[device].turn_off()

    redirect('/')

@route('/camera')
def camera(self):
        _, image = self.cam.read()
        _, data = cv2.imencode('.jpg', image)

        jpeg_base64 = base64.b64encode(data.tostring())

        return """
        <html>
        <head>
        <meta http-equiv="refresh" content="1" />
        <title>Cherrypy webcam</title>
        </head>
        <html>
        <body>
        <img src='data:image/jpeg;base64,%s' />
        <img src='data:image/jpeg;base64,%s' />
        </body>
        </html>
        """ % (jpeg_base64, jpeg_base64)

def log(msg):
	# log to file
	print msg
	f = open(logfile, 'a')
	f.write('%s %s\n' % (str(datetime.now()), msg))
	f.close()

@route('/log')
@view('log')
def viewlog():
	lines = []
	with open(logfile, 'r') as f:
		lines = f.readlines()

	return dict(lines=lines)

@route('/clearlog')
def viewlog():
	os.remove(logfile)
	redirect('/')


app = default_app.pop()
