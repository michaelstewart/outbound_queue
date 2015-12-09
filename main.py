from flask import Flask, request, jsonify
from flask.ext.api import status, exceptions
from api_exceptions import InvalidUsage
app = Flask(__name__)

import json
import Queue
q = Queue.Queue()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/add/', methods=['POST'])
def add():
    try:
        data = json.loads(request.data)
        q.put(data)
    except ValueError:
        raise InvalidUsage('Invalid json', status_code=400)
    return ''

@app.route('/get/', methods=['GET'])
def get():
    timeout = int(request.args.get('timeout', 1))
    try:
        msg = q.get(timeout=timeout)
        return jsonify(msg)
    except Queue.Empty:
        return '', status.HTTP_404_NOT_FOUND

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    app.run(debug=True)
