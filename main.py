import math
import random
import json
from typing import Tuple

# RSA Implementation 

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    d, x1, x2, y1 = 0, 0, 1, 1
    temp_phi = phi
    while e > 0:
        temp1, temp2 = divmod(temp_phi, e)
        temp_phi, e = e, temp2
        x, y = x2 - temp1 * x1, d - temp1 * y1
        x2, x1, d, y1 = x1, x, y1, y
    return d + phi if d < 0 else d

def generate_keypair(keysize):
    def get_prime():
        while True:
            num = random.randint(2**(keysize-1), 2**keysize - 1)
            if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
                return num

    p, q = get_prime(), get_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    return [pow(ord(char), e, n) for char in plaintext]

def decrypt(private_key, ciphertext):
    d, n = private_key
    return ''.join(chr(pow(char, d, n)) for char in ciphertext)

def sign(private_key, document):
    return encrypt(private_key, document)

def verify(public_key, document, signature):
    decrypted_signature = decrypt(public_key, signature)
    return decrypted_signature == document

# --- Blockchain Implementation ---

class Transaction:
    def __init__(self, sender, receiver, amount, signature):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "signature": self.signature
        }

    @staticmethod
    def from_dict(data):
        return Transaction(data['sender'], data['receiver'], data['amount'], data['signature'])

class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions

class Blockchain:
    def __init__(self, db_file="transactions.json"):
        self.chain = []
        self.transaction_pool = []
        self.db_file = db_file
        self.create_genesis_block()
        self.load_transactions_from_db()

    def create_genesis_block(self):
        genesis_block = Block("0", [])
        self.chain.append(genesis_block)

    def add_block(self, block):
        self.chain.append(block)

    def verify_transaction(self, transaction, sender_public_key):
        if not verify(sender_public_key, f"{transaction.sender}{transaction.receiver}{transaction.amount}", transaction.signature):
            raise ValueError("Signature is wrong")

    def add_transaction(self, transaction, sender_public_key):
        self.verify_transaction(transaction, sender_public_key)
        self.transaction_pool.append(transaction)
        self.save_transactions_to_db()

    def save_transactions_to_db(self):
        with open(self.db_file, "w") as file:
            transactions = [tx.to_dict() for tx in self.transaction_pool]
            json.dump(transactions, file, indent=4)

    def load_transactions_from_db(self):
        try:
            with open(self.db_file, "r") as file:
                transactions = json.load(file)
                self.transaction_pool = [Transaction.from_dict(tx) for tx in transactions]
        except FileNotFoundError:
            self.transaction_pool = []

# Wallet Implementation 
class Wallet:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key

    def create_transaction(self, receiver, amount):
        document = f"{self.public_key}{receiver}{amount}"
        signature = sign(self.private_key, document)
        return Transaction(self.public_key, receiver, amount, signature)

# Example Usage 

def main():
    # Generate keypairs for blockchain and a wallet
    blockchain_keys = generate_keypair(8)
    wallet_keys = generate_keypair(8)

    blockchain = Blockchain()
    wallet = Wallet(wallet_keys[1], wallet_keys[0])

    # Create a transaction
    transaction = wallet.create_transaction("receiver_public_key", 100)
    transaction_data = transaction.to_dict()
    print("Transaction Data:", json.dumps(transaction_data, indent=2))

    # Add the transaction to the blockchain
    try:
        blockchain.add_transaction(transaction, wallet_keys[0])
        print("Transaction added successfully.")
    except ValueError as e:
        print("Error adding transaction:", e)

if __name__ == "__main__":
    main()
