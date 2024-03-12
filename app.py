from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, World!'})


@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello, World!'})


app.run(debug=True)
