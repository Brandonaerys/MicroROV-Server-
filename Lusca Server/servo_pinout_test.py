import RPi.GPIO as gpio
import time

def Pulse2DC(Pulse):
	DC = Pulse * 5
	return DC

ServoPIN = 3
gpio.setmode(gpio.BCM)
gpio.setup(ServoPIN, gpio.OUT)

pwm = gpio.PWM(ServoPIN, 50)
#length measured in milliseconds
Min = Pulse2DC(1.1)
Max = Pulse2DC(1.9)
Center = Pulse2DC(1.5)
pwm.start(Center)
time.sleep(1)
pwm.ChangeDutyCycle(Min)
time.sleep(1)
pwm.ChangeDutyCycle(Max)
time.sleep(1)
pwm.stop()
