#!/usr/bin/env python3

import hashlib
import json
from flask import Flask, jsonify, request
from textwrap import dedent
from uuid import uuid4
from time import time
from ft_blockchain_class import blockchain


app = Flask(__name__)
node_i = str(uuid4()).replace('-', '')
bchain = blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    global pending_trans
    values = request.get_json()
    # print(values)
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    pending_trans += 1
    index = bchain.new_transaction(values['sender'], values['recipient'], values['amount'] - 0.01)
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine/<argumentstring>', methods=['GET'])
def mine(argumentstring):
    global pending_trans
    if pending_trans > 0:    
        lastblock = bchain.lastblock()
        # print(lastblock)
        lastproof = lastblock['proof']
        proof = bchain.proof_of_work(lastproof)
        # bchain.new_transaction(sender = "0", recipient = node_i, amount = 1,)
        previous_hash = bchain.hash(lastblock)
        block = bchain.new_block(proof, previous_hash, argumentstring)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transaction'],
            'proof': block['proof'],
            'previous_hash': block['previous hash'],
        }
        pending_trans -= 1
        return jsonify(response), 200
    else:
        print("No transaction to mine.")
        return jsonify("No transaction to mine."), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bchain.chain,
        'length': len(bchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    global pending_trans
    pending_trans = 0
    print("BLOCKCHAIN READY TO WORK !!!\nUSE MINERS TO WORK ON IT.")
    app.run(host='0.0.0.0', port='80')