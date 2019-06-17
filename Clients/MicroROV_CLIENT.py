import socketio
import time
import tkinter as tk
import cv2 as cv

MICRO_ROV_SERVER_NAME = "http://192.168.69.2"

OPENCV_URL = MICRO_ROV_SERVER_NAME + ":8000/stream.mjpg"
URL_SERVER_NAME = MICRO_ROV_SERVER_NAME + ":8000/wb/"
global Red
global Blue
Red = float(1.0)
Blue = float(1.0)
CameraStreamURL = URL_SERVER_NAME + str(Red) + "/" + str(Blue)
cap = cv.VideoCapture(CameraStreamURL)
video = cv.VideoCapture(OPENCV_URL)

master = tk.Tk()
master.title("Thruster and Lights")
WhiteBalance = tk.Tk()
WhiteBalance.title("White Balance")

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print('Connected')
    while True:
        ret,frame = video.read()
        cv.imshow("Stream", frame)

        key = cv.waitKey(1)
        if key & 0xFF == ord('q'):
            break

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


def ChangeSpeed(event):
    sio.emit("SpeedSnap", -1 * int(event))

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


slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed, length = 200, width=40, label="Thruster/Movement, INVERTED, DOWN=forwards")
slider.pack()
brightness = tk.Scale(master, from_=0, to=255, command=ChangeBrightness, length = 300, width=40, orient=tk.HORIZONTAL, label="Camera Lights Brightness")
brightness.pack()
WB_Red = tk.Scale(WhiteBalance, from_=4.0, to=0, command=ChangeRed, length = 300, width=40, resolution = 0.05, label="White Balance: RED")
WB_Red.pack(side=tk.LEFT)
WB_Blue = tk.Scale(WhiteBalance, from_=4.0, to=0, command=ChangeBlue, length = 300, width=40, resolution = 0.05, label="White Balance: BLUE")
WB_Blue.pack(side=tk.LEFT)
master.mainloop()
WhiteBalance.mainloop()

sio.wait()

# while True:
#     ret,frame = video.read()
#     cv.imshow("Stream", frame)
#
#     key = cv.waitKey(1)
#     if key & 0xFF == ord('q'):
#         break
