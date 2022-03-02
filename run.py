from server import socket, app
from flask_socketio import join_room, emit

# socket
@socket.on('create')
def on_join(room):
    join_room(room)

@socket.on('join')
def on_join(data):
    room = data['room']
    firstname = data['firstname']
    lastname = data['lastname']
    join_room(room)
    emit('user_joined', {'firstname': firstname, 'lastname': lastname}, room=room)

@socket.on('start_game')
def on_join(data):
    room = data['room']
    topic = data['topic']
    difficulty = data['difficulty']
    emit('init_game', {'topic': topic, 'difficulty': difficulty}, room=room)

@socket.on('send_score')
def on_send_score(data):
    room = data['room']
    firstname = data['firstname']
    lastname = data['lastname']
    score = data['score']
    emit('user_score', {'firstname': firstname, 'lastname': lastname, 'score': score}, room=room)


if __name__ == '__main__':
    socket.run(app)