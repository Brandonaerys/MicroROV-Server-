import socketio
import time
import engineio
import eventlet
import math
import RPi.GPIO as gpio

# global Speed
Speed = 0

def Pulse2DC(Pulse):
	DC = Pulse * 5
	return DC
def Speed2Pulse(Speed):
    Range = Speed * 0.4
    Pulse = Range + 1.5
    return Pulse

ServoPIN = 3
gpio.setmode(gpio.BCM)
gpio.setup(ServoPIN, gpio.OUT)

pwm = gpio.PWM(ServoPIN, 50)
#length measured in milliseconds
Min = Pulse2DC(1.1)
Max = Pulse2DC(1.9)
Center = Pulse2DC(1.5)
pwm.start(Center)

sio = socketio.Server()

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('ServerEchoTest')
def Echo(sid, data):
    sio.emit('EchoData', data)

@sio.on('SpeedChange')
def message(sid, data):
    if (data > 0) and (Speed >= 1):
        sio.emit('SpeedReport', Speed)
    elif (data < 0) and (Speed <= -1):
        sio.emit('SpeedReport', Speed)
    else:
        change = 0.1 * data
        global Speed
        Speed += change
        if Speed < 0:
            Speed = (math.ceil(Speed * 10)) / 10
        else:
            Speed = (math.floor(Speed * 10)) / 10
        sio.emit('SpeedReport', Speed)
    print(Speed)
    Output = Speed2Pulse(Speed)
    DC = Pulse2DC(Output)
    pwm.ChangeDutyCycle(DC)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)



eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
