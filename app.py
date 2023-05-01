from flask import Flask, render_template, session, request, jsonify, url_for
from flask_socketio import SocketIO, emit, disconnect

async_mode = None

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

@app.route('/')
def index():
    return render_template('index.html',async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/main')
def test_connect():
    print('Connected \n')
    emit('message_response', {'message': 'Connected'})
    
@socketio.on('open_request', namespace='/main')
def test_open():
    print('Opened \n')
    emit('message_response', {'message': 'Opened'})
    
@socketio.on('message_event', namespace='/main')
def message(message):
    print('Message received' + message['data'])
    emit('message_response', {'message': message['data']})

@socketio.on('disconnect_request', namespace='/main')
def disconnect_request():
    print('Disconnected \n')
    emit('message_response', {'message': 'Disconnected'})
    disconnect()

@socketio.on('disconnect', namespace='/main')
def test_disconnect():
    print('Client disconnected', request.sid)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80, debug=True)
