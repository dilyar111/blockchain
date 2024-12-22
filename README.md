# Blockchain Implementation Report

## **Project Overview**

This report explains the implementation of a basic blockchain system that demonstrates how blocks are created, linked together, and validated. The project is developed as an educational tool to understand the core concepts of blockchain technology, including hashing, Merkle trees, and proof-of-work mining.

---

## **Code Explanation**

The implementation includes Python code that creates a blockchain with the following features:

### **Key Components**

1. **`hash(text)` Function**
   - This function generates a SHA-256 hash for a given string.
   - Used extensively in block creation and for constructing the Merkle tree.

   Example:
   ```python
   def hash(text):
       return hashlib.sha256(text.encode('utf-8')).hexdigest()
   ```

2. **`MerkleTree` Class**
   - A Merkle tree is used to compute a single root hash for all transactions in a block.
   - This ensures data integrity and makes it efficient to verify individual transactions.

   Example Workflow:
   - Transactions are paired and hashed together recursively until only one root hash remains.
   - If there is an odd number of transactions, the last one is duplicated to form a pair.

3. **`Block` Class**
   - Represents a single block in the blockchain.
   - Contains the following attributes:
     - `index`: Position of the block in the chain.
     - `previous_hash`: Hash of the previous block, linking the chain.
     - `timestamp`: Time of block creation.
     - `transactions`: List of transactions.
     - `merkle_root`: Root hash of the transactions.
     - `nonce`: Incremental value used during mining.
   - Includes a `mine_block` method to find a hash satisfying the difficulty requirement.

4. **`Blockchain` Class**
   - Represents the entire blockchain.
   - Manages the creation of the genesis block, addition of new blocks, and validation of the chain.
   - Ensures each block's `previous_hash` matches the hash of the preceding block.

5. **Main Function**
   - Demonstrates creating a blockchain, adding blocks, and validating the chain.
   - Outputs detailed information about each block, including transactions, hashes, and mining data.

---

## **Team Members**

- **Name:** Dilyara Galymkyzy 
  - **Role:** Developed and writing report 
- **Name:** Alpamys Paninov
  - **Role:** Developed and hashed code

---

## **Program Demonstration**


![Image alt](https://github.com/dilyar111/blockchain/blob/main/Снимок%20экрана%202024-12-22%20в%2017.53.40.png) 



Here are some examples of the program's output:

1. **Genesis Block**
   - **Index:** 0
   - **Previous Hash:** 0
   - **Current Hash:** `0000abcd...` (example hash)
   - **Merkle Root:** `e3b0c442...`

2. **Subsequent Blocks**
   - **Example Transactions:**
     - "Transaction 1: Alpamys -> Dilyara: $2"
     - "Transaction 11: Erasyl -> Temirlan: $33"
   - **Nonce:** Incremented during mining to meet the difficulty target.
   - **Current Hash:** Starts with the required zeros (e.g., `0000abcd...`).

3. **Validation**
   - After adding all blocks, the blockchain is validated.
   - The program confirms whether the chain is valid by checking hashes and links.

---

## **How the Program Works**

### **Blockchain Implementation**

- **Hashing:**
  - Every block contains a hash that uniquely identifies it.
  - Hashing links the blocks together by including the previous block's hash in the current block.

- **Proof-of-Work (Mining):**
  - A difficulty level is set (e.g., 4 leading zeros).
  - The program repeatedly hashes block data with an incremented `nonce` until the resulting hash meets the difficulty criteria.

- **Merkle Tree:**
  - Transactions are grouped, and their hashes are combined recursively to produce a single Merkle root.
  - This ensures efficient transaction verification.

- **Validation:**
  - The program checks that each block's `previous_hash` matches the hash of the previous block.
  - It also recalculates the current block's hash and compares it to the stored value.

### **Workflow:**
1. The blockchain is initialized with a **genesis block**.
2. Blocks containing transactions are added one by one.
3. The chain is validated to ensure integrity.

---

## **VCS Repository Link**

The code for this project is hosted on GitHub. You can access it using the following link:
[GitHub Repository](https://github.com/dilyar111/blockchain.git)

---

## **Steps to Run the Program**

1. **Prerequisites**
   - Install Python 3.7 or higher.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/dilyar111/blockchain.git
   cd blockchain
   ```

3. **Run the Program**
   Execute the following command in the terminal:
   ```bash
   python blockchain.py
   ```

4. **Expected Output**
   - The program will display information about each block in the chain:
     - **Block Index**
     - **Hash Data**
     - **Merkle Root**
     - **Transactions**
     - **Mining Nonce**
   - It will also confirm whether the blockchain is valid.

5. **Add More Transactions**
   - You can modify the `main` function to add new transactions and observe the changes.

---

This project serves as a foundation for understanding blockchain mechanics and can be expanded further to include advanced features like decentralized consensus or smart contracts.


