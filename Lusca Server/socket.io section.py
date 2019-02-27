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
    if (data > 0) and (Speed >= 1):
        sio.emit('SpeedReport', Speed)
    elif (data < 0) and (Speed <= -1):
        sio.emit('SpeedReport', Speed)
    else:
        change = 0.1 * data
        global Speed
        Speed += change
        sio.emit('SpeedReport', Speed)
    print(Speed)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)



eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
