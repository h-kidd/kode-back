from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, send

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}

if __name__ == '__main__':
    socketio.run(app)