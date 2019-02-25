import socketio

import engineio
import eventlet

sio = socketio.Server()

app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

Speed = 0

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('ServerEchoTest')
def Echo(sid, data):
    sio.emit('EchoData', data)

@sio.on('ChangeSpeed')
def message(sid, data):
    Speed += data
    sio.emit('SpeedReport', Speed)
    print(Speed)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
