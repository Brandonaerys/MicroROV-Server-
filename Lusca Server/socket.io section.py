import socketio
import time
import engineio
import eventlet

# global Speed
Speed = 0

sio = socketio.Server()

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('ServerEchoTest')
def Echo(sid, data):
    sio.emit('EchoData', data)

@sio.on('SpeedChange')
def message(sid, data):
    if (data > 0) and (Speed >= 10):
        sio.emit('SpeedReport', Speed)
    elif (data < 0) and (Speed <= -10):
        sio.emit('SpeedReport', Speed)
    else:
        global Speed
        global Output
        Speed += data
        Output = 0.1 *  Speed
        sio.emit('SpeedReport', Output)
    print(Speed)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)



eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
