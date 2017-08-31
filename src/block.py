import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash

        # we could be setting a new blockchain for consensus. If we already have the hash don't calculate a new one
        if hash:
            self.hash = hash
        else:
            self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(self.previous_hash)
        )
        return sha.hexdigest()

    def __repr__(self):
        return "<Block index:%s timestamp:%s data:%s hash:%s>" % (self.index, self.timestamp, self.data, self.hash)