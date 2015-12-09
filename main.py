from flask import Flask
app = Flask(__name__)

import Queue
q = Queue.Queue()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/add')
def add():
    return ''

@app.route('/get')
def get():
    return ''

@app.route('/delete')
def delete():
    return ''


if __name__ == '__main__':
    app.run()