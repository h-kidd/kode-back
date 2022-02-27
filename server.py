from enum import unique
from pydoc_data.topics import topics
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config

#flaskjwt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
# "///" is relative path from current file.
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:password@kode.c4rgiwquolnv.eu-west-2.rds.amazonaws.com:5432/kode"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
socket = SocketIO(app, cors_allowed_origins="*")
# app.config.from_object(config("APP_SETTINGS"))

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Creating db instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), nullable=False )
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False )
    # homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), nullable=False )
    # completed_id = db.Column(db.Integer, db.ForeignKey("completed.id"), nullable=False )

    # homework = db.Column(db.String(10), nullable=False, default="0")
    # completed = db.Column(db.String(10), nullable=False, default="0")

    # how object is printed
    def __repr__(self):
        return f"Student('{self.firstname}','{self.lastname} ')"

# Teacher and Student relationship: one to many.
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    #students attribute has relationship to Student model,
    #backref is similar to adding another column to the Student model.
    #Allows when there is a teacher, use student attribute to get the Student
    #linked to teacher. Lazy arg is used to load necessary data in one go.
    students = db.relationship("Student", backref="teacher", lazy=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Teacher('{self.firstname}','{self.lastname} ')"

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Student.query.filter_by(id=identity).one_or_none()

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship("Student", backref="homework", lazy=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Homework('{self.completed}','{self.score} ')"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question = db.Column(db.ARRAY(db.String), server_default="{}")
    answer = db.Column(db.ARRAY(db.String), server_default="{}")
    options = db.Column(db.ARRAY(db.String), server_default="{}")
    

    def __repr__(self):
        return f"Question('{self.topic}','{self.difficulty} ','{self.question} ','{self.answer} ','{self.options} ')"


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = Student.query.filter_by(username=username).one_or_none() or Teacher.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

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