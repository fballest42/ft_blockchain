import time
import json
import hashlib
from urllib.parse import urlparse
import requests

class blockchain(object):
    def __init__(self):
        self.chain = []
        self.trasaction = []
        self.nodes = set()
        self.end_hash = "4242"
        self.new_block(old_hash = 1, proof = 100)
    
    def new_block(self, proof, old_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transaction': self.trasaction,
            'proof': proof,
            'previous hash': old_hash}
        self.transaction = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.transaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount})
        return self.lastblock()['index'] + 1
    
    def hash(self, block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def lastblock(self):
        return self.chain[-1]
    
    def proof_of_work(self, lastproof = None):
        proof = lastproof
        self.end_hash = str("4242" * (1 + (len(self.chain) // 10)))
        while self.valid_proof(lastproof, proof, self.end_hash) is False:
            proof += 1
        return proof
    
    def valid_proof(self, lastproof, proof, end_hash):
        guess = f'{lastproof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        if guess_hash[(-1) * (len(end_hash)):]:
            print(guess_hash)
        return guess_hash[(-1) * (len(end_hash)):] == end_hash

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        lastblock = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{lastblock}')
            print(f'{block}')
            print("\n*********************************************\n")
            if block['old_hashh'] != self.hash(lastblock):
                return False
            if not self.valid_proof(lastblock['proof'], block['proof'], self.end_hash):
                return False
            lastblock = block
            current_index += 1
        return True
    
    def solve_conflicts(self):
        other = self.nodes
        new_chain = None
        max_len = len(self.chain)
        for node in other:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                lenght = response.json()['lenght']
                chain = response.json()['chain']
                if lenght > max_len and self.valid_chain(chain):
                    max_len =lenght
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True
        return False
