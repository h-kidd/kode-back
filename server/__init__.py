from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_marshmallow import Marshmallow

#flaskjwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"]="DATABASEURL"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!


app.config.from_object(config("APP_SETTINGS"))
socket = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from server import routes