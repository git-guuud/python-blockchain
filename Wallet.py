from BlockChain import Account,Block,Trasanction
import os
import json
import time

GENESISHASH = "0000000399c6aea5ad0c709a9bc331a3ed6494702bd1d129d8c817a0257a1462"

WALLET_PATH = "./wallet.json"
ACCOUNT = Account()

if os.path.exists(WALLET_PATH):
    with open(WALLET_PATH, "r") as ledger:
        data = json.loads(ledger.read())
        ACCOUNT.__dict__ = data
else:
    with open(WALLET_PATH, "w") as ledger:
        ledger.write(json.dumps(ACCOUNT.__dict__))

def mine():
    nonce=0
    block = Block(GENESISHASH, nonce, ACCOUNT.publicKey)
    while not block.mine():
        nonce+=1
        block.header.nonce = nonce

mine()

def make_transaction(recipient_address, amount):
    t = Trasanction(time.time(), )