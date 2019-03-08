import socketio
import time
import engineio
import eventlet
import math
import RPi.GPIO as gpio
import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server


global Speed
Speed = 0
def Speed2Pulse(Speed):
    Range = Speed * 0.1 * 0.4
    Pulse = Range + 1.5
    return Pulse
def Pulse2DC(Pulse):
	DC = Pulse * 5
	return DC

def PinOutput():
    ServoPIN = 4
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

    # @sio.on('SpeedChange')
    # def message(sid, data):
    #     if (data > 0) and (Speed >= 10):
    #         sio.emit('SpeedReport', Speed)
    #     elif (data < 0) and (Speed <= -10):
    #         sio.emit('SpeedReport', Speed)
    #     else:
    #         global Speed
    #         Speed += data
    #         sio.emit('SpeedReport', Speed)
    #     print(Speed)
    #     Output = Speed2Pulse(Speed)
    #     DC = Pulse2DC(Output)
    #     pwm.ChangeDutyCycle(DC)
    #     print(Output)
    @sio.on('SpeedSnap')
    def ChangeSpeed(sid, data):
        global Speed
        Speed = data
        sio.emit('SpeedReport', Speed)
        print(Speed)
        Output = Speed2Pulse(Speed)
        DC = Pulse2DC(Output)
        pwm.ChangeDutyCycle(DC)
        print(Output)

    @sio.on('disconnect')
    def disconnect(sid):
        print('disconnect ', sid)

    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

PAGE="""\
<html>
<head>
<title>Raspberry Pi Camera Stream</title>
</head>
<body>
<center><h1>Raspberry Pi Camera Stream</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
</body>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

camera = picamera.PiCamera(resolution='640x640', framerate=15)
output = StreamingOutput()
camera.rotation = 90
camera.start_recording(output, format='mjpeg')

try:
    PinOutput()
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
except KeyboardInterrupt:
    pwm.stop()
    gpio.cleanup()
    camera.stop_recording()
finally:
    pwm.stop()
    gpio.cleanup()
    camera.stop_recording()
