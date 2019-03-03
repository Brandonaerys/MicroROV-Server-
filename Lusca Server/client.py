import socketio
import time
import tkinter as tk

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

sio.connect('http://192.168.69.2:5000')



def SpeedUp(event):
    sio.emit('SpeedChange', 1)

def SpeedDown(event):
    sio.emit('SpeedChange', -1)

def ChangeSpeed(event):
    sio.emit("SpeedSnap", int(event))

def Exit(event):
    pass
# sio.wait()



widget = tk.Button(master, text='SpeedUp = Mouse1, SpeedDown = Mouse2')
widget.pack()
slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed)
slider.pack()
widget.bind('<Button-1>', SpeedUp)
widget.bind('<Button-3>', SpeedDown)
widget.bind('<Button-2>', Exit)
master.mainloop()

sio.wait()
