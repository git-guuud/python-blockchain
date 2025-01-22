import hashlib
import json
import random
import ecdsa

VERSION = "0.0.1a"

GENESISHASH = "0000000399c6aea5ad0c709a9bc331a3ed6494702bd1d129d8c817a0257a1462"
LEDGER_PATH = "./ledger.json"

class block():
    def __init__(self, prevBlockHash, nonce, transactions):
        self.header = header(prevBlockHash, nonce)
        self.transactions = transactions

    def hash(self):
        return hashlib.sha256(json.dumps(self.__dict__.encode())).hexdigest()

class header():
    def __init__(self, prevBlockHash, nonce):
        self.version = VERSION
        self.prevBlockHash = prevBlockHash
        self.nonce = nonce

class Account():
    def __init__(self):
        self.privateKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.publicKey = self.privateKey.get_verifying_key().to_string().hex()
        self.privateKey = self.privateKey.to_string().hex()
        self.address = hashlib.sha256(self.publicKey.encode()).hexdigest()
        self.balance = 0
    
    def __str__(self):
        return f"PrivateKEY: {self.privateKey}\n PublicKEY: {self.publicKey}\n Address: {self.address} \n Balance: {self.balance}"


print(Account())