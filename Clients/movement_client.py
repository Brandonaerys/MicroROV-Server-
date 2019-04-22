import socketio
import time
import tkinter as tk
import cv2 as cv

MICRO_ROV_SERVER_NAME = "http://192.168.69.2"

master = tk.Tk()
master.title("MicroROV")
WhiteBalance = tk.Tk()
WhiteBalance.title("White Balance")

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected')

@sio.on('EchoData')
def PrintEcho(data):
    print(data)


@sio.on('disconnect')
def on_disconnect():
    print('Disconnected')

@sio.on('SpeedReport')
def ReportSpeed(Speed):
    print('Current Speed:', Speed)

sio.connect(MICRO_ROV_SERVER_NAME + ":5000")



# def SpeedUp(event):
#     sio.emit('SpeedChange', 1)
#
# def SpeedDown(event):
#     sio.emit('SpeedChange', -1)
URL_SERVER_NAME = MICRO_ROV_SERVER_NAME + ":8000/wb/"
global Red
global Blue
Red = float(1.0)
Blue = float(1.0)
CameraStreamURL = URL_SERVER_NAME + str(Red) + "/" + str(Blue)
cap = cv.VideoCapture(CameraStreamURL)

def ChangeSpeed(event):
    sio.emit("SpeedSnap", int(event))

def ChangeBrightness(event):
    sio.emit("BrightnessChange", int(event))

def ChangeRed(event):
    global Red
    Red = float(event)
    CameraStreamURL = URL_SERVER_NAME + str(Red) + "/" + str(Blue)
    cap = cv.VideoCapture(CameraStreamURL)
    print("RedChange:", event)

def ChangeBlue(event):
    global Blue
    Blue = float(event)
    CameraStreamURL = URL_SERVER_NAME + str(Red) + "/" + str(Blue)
    cap = cv.VideoCapture(CameraStreamURL)
    print("BlueChange:", event)


def Exit(event):
    pass


slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed, length = 200, width=40)
slider.pack()
brightness = tk.Scale(master, from_=0, to=255, command=ChangeBrightness, length = 300, width=40, orient=tk.HORIZONTAL)
brightness.pack()
WB_Red = tk.Scale(WhiteBalance, from_=4.0, to=0, command=ChangeRed, length = 300, width=40, resolution = 0.05)
WB_Red.pack()
WB_Blue = tk.Scale(WhiteBalance, from_=4.0, to=0, command=ChangeBlue, length = 300, width=40, resolution = 0.05)
WB_Blue.pack()
master.mainloop()
WhiteBalance.mainloop()

sio.wait()
