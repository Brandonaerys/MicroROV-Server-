import tkinter as tk



def SpeedUp(event):
    print("Speed +1")

def SpeedDown(event):
    print("Speed -1")

def Exit(event):
    pass

widget = tk.Button(None, text='Input')
widget.pack()
widget.bind('<Button-1>', SpeedUp)
widget.bind('<Button-3>', SpeedDown)
widget.bind('<Button-2>', Exit)
widget.mainloop()
