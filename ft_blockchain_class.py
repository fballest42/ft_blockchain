import time
import json
import hashlib
from urllib.parse import urlparse
import requests

class blockchain(object):
    def __init__(self):
        self.chain = []
        self.trasaction = []
        self.chain.append({
            'index': 1,
            'timestamp': time.time(),
            'transaction': self.trasaction,
            'proof': 0,
            'previous hash': 0,
            'hash' : self.proof_of_work(1),
            'miner': 'INITIAL_BLOCK',
            'reward': 0.0,
        })
        self.nodes = set()
        self.end_hash = "4242"
        self.miner = None
        self.reward = 0.01
        # self.new_block(old_hash = 1, proof = 100)
    
    def new_block(self, proof, old_hash = None, miner = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transaction': self.trasaction,
            'proof': proof,
            'previous hash': self.lastblock()['hash'],
            'hash' : self.proof_of_work(proof),
            'miner': miner,
            'reward': self.reward,
            }
        self.trasaction = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.trasaction.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount})
        return self.lastblock()['index'] + 1
    
    def hash(self, block):
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def lastblock(self):
        return self.chain[-1]
    
    def proof_of_work(self, lastproof):
        proof = 0
        self.end_hash = str("4242" * (1 + (len(self.chain) // 10)))
        guess = f'{lastproof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        while (guess_hash[(-1) * (len(self.end_hash)):]) != "4242":
            guess = f'{lastproof}{proof}'.encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            # if guess_hash[(-1) * (len(self.end_hash)):]:
            #     print(guess_hash)
            proof += 1
        # self.chain.pop()
        return guess_hash
    
    # def valid_proof(self, lastproof, proof, end_hash):
    #     guess = f'{lastproof}{proof}'.encode()
    #     guess_hash = hashlib.sha256(guess).hexdigest()
    #     if guess_hash[(-1) * (len(end_hash)):]:
    #         print(guess_hash)
    #     return guess_hash[(-1) * (len(end_hash)):] == end_hash

    def valid_chain(self, chain):
        lastblock = chain[0]
        current_index = 0
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{lastblock}')
            print(f'{block}')
            print("\n*********************************************\n")
            if block['old_hash'] != lastblock['previous hash']:
                return False
            if not self.proof_of_work(lastblock['proof'], block['proof'], self.end_hash):
                return False
            lastblock = block
            current_index += 1
        return True
