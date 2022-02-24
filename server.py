from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}

if __name__ == '__main__':
    app.run(debug=True)