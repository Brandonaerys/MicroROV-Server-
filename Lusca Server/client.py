import socketio
import time
from tkinter import *

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
    print(Speed)

sio.connect('http://localhost:5000')



def speedup(event):
    sio.emit('SpeedChange', 1)

def speeddown(event):
    sio.emit('SpeedChange', -1)

def exit(event):
    pass


widget = Button(None, text='Input')
widget.pack()
widget.bind('<Button-1>', speedup)
widget.bind('<Button-3>', speeddown)
widget.bind('<Button-2>', exit)
widget.mainloop()

sio.wait()
