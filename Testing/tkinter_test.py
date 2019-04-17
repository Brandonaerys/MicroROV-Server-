import tkinter as tk


master = tk.Tk()
master.title("MicroROV")


def SpeedUp(event):
    print('SpeedChange ', "+1")

def SpeedDown(event):
    print('SpeedChange ', "-1")

def Exit(event):
    pass
# sio.wait()

def ChangeSpeed(event):
    print("SpeedSnap ", event)
def ChangeBrightness(event):
    print("Brightness", event)

widget = tk.Button(master, text='SpeedUp = Mouse1, SpeedDown = Mouse2')
widget.pack()
slider = tk.Scale(master, from_=10, to=-10, command=ChangeSpeed, length = 200, width=40)
slider.pack()
brightness = tk.Scale(master, from_=0, to=255, command=ChangeBrightness, length = 300, width=40, orient=tk.HORIZONTAL)
brightness.pack()
master.mainloop()
