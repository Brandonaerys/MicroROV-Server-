from tkinter import *

def click(event):
    print("Single Click, Button-l")

def speedup(event):
    sio.emit('SpeedChange', 1)

def speeddown(event):
    sio.emit('SpeedChange', -1)

def exit(event):
    pass


widget = Button(None, text='Mouse Clicks')
widget.pack()
widget.bind('w', speedup)
widget.bind('s', speeddown)
widget.bind('q', exit)
widget.mainloop()
