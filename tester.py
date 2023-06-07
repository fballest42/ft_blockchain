#!/usr/bin/env python3

import requests
import json
import random
import string
serverUrl = "http://0.0.0.0:80"

def sendTransaction():
    try:
        sender = input("Enter the sender: ")
        recipient = input("Enter the recipient: ")
        amount = float(input("Enter the amount: "))
        while amount < 0.01:
            amount = float(input("Enter the amount: "))
    except:
        print("Error: Invalid imput. Retry it.")
        return
    transactionData = {'sender': sender,'recipient': recipient,'amount': amount}
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(serverUrl + "/transactions/new", data=json.dumps(transactionData), headers=headers)
        print(response.status_code, response.json())
    except:
        print("ERROR: Client failed to send transaction")
def mineBlock(miner):
    try:
        response = requests.get(serverUrl + "/mine/" + miner)
        print(response.text)
    except:
        print("ERROR: Failed to receive transaction")
        
def requestChain():
    try:
        response = requests.get(serverUrl + "/chain")
        print(response.text)
    except:
        print("ERROR: Failed to receive transaction")


if __name__ == '__main__':
    miner = ''
    for i in range (10):
        miner += str(random.choice(string.ascii_lowercase))
    print("Miner --> ", miner)
    while True:
        print("1. New transaction")
        print("2. Mine")
        print("3. Chain")
        print("0. Exit")
        clientInput = input("Enter test value: ")
        if clientInput == "1":
            sendTransaction()
        elif clientInput == "2":
            mineBlock(miner)
        elif clientInput == "3":
            requestChain()
        elif clientInput == "0":
            print("Bye!")
            break
        else:
            print("Value not found")