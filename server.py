from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}

@socket.on('create')
def on_join(room):
    socket.join_room(room)

@socket.on('join')
def on_join(data):
    room = data['room']
    name = data['name']
    socket.join_room(room)
    socket.emit('user_joined', name, room=room)

@socket.on('start_game')
def on_join(data):
    room = data['room']
    socket.emit('init_game', "Game start!", room=room)

@socket.on('send_score')
def on_send_score(data):
    room = data['room']
    name = data['name']
    score = data['score']
    socket.emit('user_score', {'name': name, 'score': score}, room=room)

if __name__ == '__main__':
    socket.run(app)