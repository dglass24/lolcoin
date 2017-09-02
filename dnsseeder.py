from flask import Flask
from flask import request
from flask import jsonify
from src.config import Config

import requests
import json

node = Flask(__name__)

config = Config()

peers = set()

@node.route('/register', methods=['POST'])
def post_register():
    if request.method == 'POST':
        existing_peers = peers.copy()
        existing_peers.discard(request.referrer)
        peers.add(request.referrer)

        # broadcast new peer to all existing peers
        for peer in existing_peers:
            try:
                requests.post(peer + '/addhost', json=json.dumps({'host': request.referrer}))
            except:
                # TODO: log failure
                pass

        return jsonify(list(existing_peers))

@node.route('/deregister', methods=['POST'])
def post_deregister():
    if request.method == 'POST':
        peers.discard(request.referrer)

        # broadcast new peer to all existing peers
        for peer in peers:
            try:
                requests.post(peer + '/removehost', json=json.dumps({'host': request.referrer}))
            except:
                # TODO: log failure
                pass

if __name__ == '__main__':
    node.run(host=config.get('host'), port=config.get('port'))











