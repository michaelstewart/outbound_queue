#!/usr/bin/python

from flask import Flask, request, jsonify
from flask.ext.api import status, exceptions
from api_exceptions import InvalidUsage
app = Flask(__name__)

import atexit
import json
import Queue
from persistent_queue import PersistentQueue

QUEUE_FILENAME = 'queue.p'
q = PersistentQueue(QUEUE_FILENAME)

@app.route('/add/', methods=['POST'])
def add():
    try:
        data = json.loads(request.data)
        if type(data) == list:
            messages = data
        else:
            messages = [data]
        for message in messages:
            q.put(message)
    except ValueError:
        raise InvalidUsage('Invalid json', status_code=400)
    return ''

@app.route('/get/', methods=['GET'])
def get():
    num = int(request.args.get('num', 1))
    messages = []
    try:
        for i in xrange(num):
            message = q.get(block=False)
            messages.append(message)
    except Queue.Empty:
        pass # We expect to hit this

    if len(messages) == 0:
        status_code = status.HTTP_404_NOT_FOUND
    else:
        status_code = status.HTTP_200_OK
    return jsonify({'messages': messages}), status_code

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def persist_on_exit():
    ''' this is run upon exit '''
    print "Exiting, saving queue."
    # TODO implement

if __name__ == '__main__':
    atexit.register(persist_on_exit)
    app.run(debug=True)

