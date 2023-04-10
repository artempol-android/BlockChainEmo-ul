import os
import threading

from flask import Flask, request, jsonify

from Node import Node

app = Flask(__name__)
node = Node()
t = threading.Thread(target=node.chainBuild)

host = '0.0.0.0'
port = 8080
neighbors = [8081, 8082]
master_mode = False

if 'PORT' in os.environ:
    port = int(os.environ['PORT'])
    node.port = port
if 'NEIGHBORS' in os.environ:
    neighbors = os.environ['NEIGHBORS'].split(',')
    node.neighbors = neighbors
if 'NONCE_MODE' in os.environ:
    node.mode = os.environ['NONCE_MODE']
if 'MASTER' in os.environ:
    master_mode = os.environ['MASTER'].lower() == "true"
    if master_mode:
        node.stop = False
        t.start()


@app.route('/')
def hello():
    return "Hello!"


@app.route('/add_block', methods=['POST'])
def add_block():
    global t
    block_data = request.json
    if block_data['index'] > node.getLastIndex():
        if t.is_alive():
            node.stop = True
            t.join()
        res = node.fixMinority(block_data['index'], request.environ['REMOTE_ADDR'], block_data['port'])
        t = threading.Thread(target=node.chainBuild)
        node.stop = False
        t.start()
        if res:
            return "success"
        else:
            return "denied"
    else:
        return "denied"


@app.route('/get_block')
def get_block():
    block_index = int(request.args['index'])
    block = node.getBlockFromChain(block_index)
    return jsonify(
        index=block.index,
        prev_hash=block.prev_hash,
        data=block.data,
        nonce=block.nonce,
        hash=block.hash
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
