import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # this can be document hash or metadata
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        hash_str = (str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode()
        sha.update(hash_str)
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), new_data, latest_block.hash)
        self.chain.append(new_block)
        return new_block

# Example usage
if __name__ == "__main__":
    my_blockchain = Blockchain()

    # Simulate hashing a document content string
    document_content = "Example legal document content"
    document_hash = hashlib.sha256(document_content.encode()).hexdigest()

    new_block = my_blockchain.add_block(document_hash)
    print(f"Added block with hash: {new_block.hash}")
