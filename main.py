import os

from flask import Flask

from Node import Node

app = Flask(__name__)
node = Node()

host = '0.0.0.0'
port = 8080
neighbours = [8081, 8082]
master_mode = False

if 'HOST' in os.environ:
    host = os.environ['HOST']
if 'PORT' in os.environ:
    port = int(os.environ['PORT'])
if 'NEIGHBOURS' in os.environ:
    neighbours = os.environ['NEIGHBOURS'].split(',')
if 'NONCE_MODE' in os.environ:
    node.mode = os.environ['NONCE_MODE']
if 'MASTER' in os.environ:
    master_mode = os.environ['MASTER'].lower() == "true"


@app.route('/')
def index():
    return 'Hello World'


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)  # add debug mode
