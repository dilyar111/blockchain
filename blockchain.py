import hashlib
from os import name
import time

def hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_merkle_tree(transactions)

    def build_merkle_tree(self, transactions):
        if len(transactions) == 1:
            return hash(transactions[0])

        new_level = []
        for i in range(0, len(transactions), 2):
            left = transactions[i]
            right = transactions[i + 1] if i + 1 < len(transactions) else left
            new_level.append(hash(left + right))

        return self.build_merkle_tree(new_level)

class Block:
    def __init__(self, index, previous_hash, transactions):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.transactions = transactions
        self.merkle_tree = MerkleTree(transactions)
        self.merkle_root = self.merkle_tree.root
        self.nonce = 0
        self.hash = None

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while True:
            self.hash = hash(f"{self.index}{self.previous_hash}{self.timestamp}{self.merkle_root}{self.nonce}")
            if self.hash[:difficulty] == target:
                break
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, '0', ["Genesis Block"])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), last_block.hash, transactions)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash != hash(f"{current_block.index}{current_block.previous_hash}{current_block.timestamp}{current_block.merkle_root}{current_block.nonce}"):
                return False

        return True

def main():
    blockchain = Blockchain(difficulty=4)

    transactions1 = [f"Transaction {i + 1}: Alpamys -> Dilyara: ${i * 2}" for i in range(10)]
    blockchain.add_block(transactions1)

    transactions2 = [f"Transaction {i + 11}: Erasyl -> Temirlan: ${i * 3}" for i in range(10)]
    blockchain.add_block(transactions2)

    is_valid = blockchain.validate_blockchain()
    print("BLOCKCHAIN VALIDATION: ", is_valid)

    for block in blockchain.chain:
        print("Block Index:", block.index)
        print("Previous Hash:", block.previous_hash)
        print("Current Hash:", block.hash)
        print("Merkle Root:", block.merkle_root)
        print("Nonce:", block.nonce)
        print("Transactions:", block.transactions)

    transactions3 = [f"Transaction {i + 21}: Arsen -> Adil: ${i * 5}" for i in range(10)]
    blockchain.add_block(transactions3)

    print("\n ADDED NEW BLOCK: ")
    for block in blockchain.chain:
        print("Block Index:", block.index)
        print("Previous Hash:", block.previous_hash)
        print("Current Hash:", block.hash)
        print("Merkle Root:", block.merkle_root)
        print("Nonce:", block.nonce)
        print("Transactions:", block.transactions)

if __name__ == "__main__":
    main()