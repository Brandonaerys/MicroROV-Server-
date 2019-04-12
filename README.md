# MicroROV_Server

Server programs on raspberry pi run on startup

The client programs on the client side (LAPTOP) can access and control the MicroROV
To run the only program to control the Micro ROV, on the laptop, go Desktop -> GitHub - Shortcut -> MicroROV_Server -> Servers
then run the python file movement_server.py by double clicking it

A slider will appear which can be controlled using the mouse/pointer of the laptop.  This slider will control the forwards and backwards movements of the MicroROV

To access the camera stream, use the address "http://192.168.69.2:8000/stream.mjpg"
The white balance of the camera can be tuned by entering the address "http://192.168.69.2:8000/wb/1.0/1.0" in a browser, replacing the two numbers with the desired values of red and blue balance, in that order (between 0.1 and 7.5).  Once this is changed, the white balance will change automatically as well on any other instances of "http://192.168.69.2:8000/stream.mjpg".
