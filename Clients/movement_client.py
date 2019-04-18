import socketio
import time
import tkinter as tk

master = tk.Tk()
master.title("MicroROV")
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

sio.connect('http://192.168.0.234:5000')



# def SpeedUp(event):
#     sio.emit('SpeedChange', 1)
#
# def SpeedDown(event):
#     sio.emit('SpeedChange', -1)

def ChangeSpeed(event):
    sio.emit("SpeedSnap", int(event) - 2)

def ChangeBrightness(event):
    sio.emit("BrightnessChange", int(event))

def Exit(event):
    pass
# sio.wait()



# widget = tk.Button(master, text='SpeedUp = Mouse1, SpeedDown = Mouse2')
# widget.pack()
# widget.bind('<Button-1>', SpeedUp)
# widget.bind('<Button-3>', SpeedDown)
# widget.bind('<Button-2>', Exit)
slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed, length = 200, width=40)
slider.pack()
brightness = tk.Scale(master, from_=0, to=255, command=ChangeBrightness, length = 300, width=40, orient=tk.HORIZONTAL)
brightness.pack()
master.mainloop()

sio.wait()
