from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config


app = Flask(__name__)
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")
app.config.from_object(config("APP_SETTINGS"))

# "///" is relative path from current file.
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///kode.db"

# Creating db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Student(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(65), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    homework = db.Column(db.String(10), nullable=False, default="0")
    completed = db.Column(db.String(10), nullable=False, default="0")

    # how object is printed
    def __repr__(self):
        return f"Student('{self.firstname}','{self.lastname} ')"

# Teacher and Student relationship: one to many.
class Teacher(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    #students attribute has relationship to Student model,
    #backref is similar to adding another column to the Student model.
    #Allows when there is a teacher, use student attribute to get the Student
    #linked to teacher. Lazy arg is used to load necessary data in one go.
    students = db.relationship("Student", backref="student", lazy=True)






# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}

# socket
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