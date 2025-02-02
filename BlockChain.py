import hashlib
import json
import ecdsa
import plyvel

VERSION = "0.0.1a"

GENESISHASH = "0000000399c6aea5ad0c709a9bc331a3ed6494702bd1d129d8c817a0257a1462"
LEDGER_DB = plyvel.DB('ledger', create_if_missing=True)

class Block():
    def __init__(self, prevBlockHash, nonce, minerPK):
        self.header = header(prevBlockHash, nonce)
        self.transactions = [CoinBaseTransaction(minerPK)]

    def addTransaction(self, transaction):
        self.transactions.append(transaction)

    def hash(self):
        return hashlib.sha256(self.toJSON().encode()).hexdigest()

    def toJSON(self):
        return json.dumps(self.header.__dict__) + f"{[i.toJSON()+'\n' for i in self.transactions]}"

    def mine(self):
        if self.hash().startswith("000000"):
            LEDGER_DB.put(self.hash(), self.toJSON())
            return True
        return False


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


class Trasanction():
    def __init__(self, timestamp, inputs, outputs):
        self.timestamp = timestamp
        self.inputs = inputs
        self.outputs = outputs
    
    def toJSON(self):
        # return f'{{"timestamp": {self.timestamp},\n"inputs":{[i.toJSON() for i in self.inputs]},\n"outputs":{[i.toJSON() for i in self.outputs]}}}'
        d = self.__dict__
        d["inputs"] = [i.toJSON() for i in self.inputs]
        d["outputs"] = [i.toJSON() for i in self.outputs]
        return json.dumps(d)


class Input():
    def __init__(self, serial, prevTransactionHash, refOutput, signature):
        self.serial = serial
        self.prevTransactionHash = prevTransactionHash
        self.outputIndex = refOutput
        self.signature = signature
    
    def toJSON(self):
        return json.dumps(self.__dict__)


class Output():
    def __init__(self, inputSerial, amount, address):
        self.inputSerial = inputSerial
        self.amount = amount
        self.address = address

    def toJSON(self):
        return json.dumps(self.__dict__)

class Stack():
    def __init__(self, amount, transactionHash, reciever_address):
        self.amount = amount
        self.transactionHash = transactionHash
        self.reciever = reciever_address
        


    def toJSON(self):
        return json.dumps(self.__dict__)
        

class CoinBaseTransaction():
    def __init__(self, reciever_address):
        self.amount = 1
        self.reciever = reciever_address
        self.stack = Stack(1, reciever_address)
    
    def toJSON(self):
        d = self.__dict__
        d["stack"] = self.stack.toJSON()
        return json.dumps(d)