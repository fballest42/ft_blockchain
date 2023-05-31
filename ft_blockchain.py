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
    values = request.get_json()
    print(values)
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    index = bchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/mine', methods=['GET'])
def mine():
    lastblock = bchain.lastblock()
    print(lastblock)
    lastproof = lastblock['proof']
    proof = bchain.proof_of_work(lastproof)
    bchain.new_transaction(sender = "0", recipient = node_i, amount = 1,)
    previous_hash = bchain.hash(lastblock)
    block = bchain.new_block(proof, previous_hash)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': bchain.chain,
        'length': len(bchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400
    for node in nodes:
        bchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(bchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = bchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': bchain.chain,
            }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': bchain.chain,
            }
    return jsonify(response), 200

if __name__ == '__main__':
    print("Please, insert the port to work on: ")
    port_i = int(input())
    app.run(host='0.0.0.0', port=port_i)
