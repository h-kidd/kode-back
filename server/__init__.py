from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from decouple import config
from flask_marshmallow import Marshmallow
from datetime import timedelta

#flaskjwt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
# app.config["SQLALCHEMY_DATABASE_URI"]="DATABASEURL"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(config("APP_SETTINGS"))
app.config["JWT_SECRET_KEY"] = config("SECRET_KEY")  # Change this!
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)


socket = SocketIO(app, cors_allowed_origins="https://kode-client.netlify.app")
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

from server import routes