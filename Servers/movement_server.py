import socketio
import time
import engineio
import eventlet
import math
import RPi.GPIO as gpio
from neopixel import *
import argparse

# LED strip configuration
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Animation functions
def WhiteColor(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255,255,255))
        strip.show()

if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    WhiteColor(strip)
    print('Ctrl+C to quit.')
    try:
        global Speed
        Speed = 0
        def Speed2Pulse(Speed):
            Range = Speed * 0.1 * 0.4
            Pulse = Range + 1.5
            return Pulse
        def Pulse2DC(Pulse):
        	DC = Pulse * 5
        	return DC


        ServoPIN = 17
        gpio.setmode(gpio.BCM)
        gpio.setup(ServoPIN, gpio.OUT)

        pwm = gpio.PWM(ServoPIN, 50)
        #length measured in milliseconds
        Min = Pulse2DC(1.1)
        Max = Pulse2DC(1.9)
        Center = Pulse2DC(1.5)
        pwm.start(Center)

        strip.show()

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

        @sio.on("BrightnessChange")
        def Brightness(sid, data):
            for i in range (strip.numPixels()):
                strip.setPixelColor(i, Color(data,data,data))
                strip.show()


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
    except KeyboardInterrupt:
        pwm.stop()
        gpio.cleanup()
