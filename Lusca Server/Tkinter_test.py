import tkinter as tk


master = tk.Tk()


def SpeedUp(event):
    print('SpeedChange ', "+1")

def SpeedDown(event):
    print('SpeedChange ', "-1")

def Exit(event):
    pass
# sio.wait()

def ChangeSpeed(event):
    print("SpeedSnap ", event)

widget = tk.Button(master, text='SpeedUp = Mouse1, SpeedDown = Mouse2')
widget.pack()
slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed)
slider.pack()
widget.bind('<Button-1>', SpeedUp)
widget.bind('<Button-3>', SpeedDown)
widget.bind('<Button-2>', Exit)
master.mainloop()
