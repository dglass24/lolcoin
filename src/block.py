import hashlib as hasher
import json

class Block:
    def __init__(self, index, timestamp, data, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def hash_block(self, previous_hash):
        if self.hash is not None:
            raise "Can't rehash block that already has a hash"

        sha = hasher.sha256()
        sha.update(
            str(self.index) +
            str(self.timestamp) +
            str(self.data) +
            str(previous_hash)
        )
        self.hash = sha.hexdigest()

    def __repr__(self):
        return "<Block index:%s timestamp:%s data:%s hash:%s>" % (self.index, self.timestamp, self.data, self.hash)

    def to_json(self):
        return json.dumps({
            'index': self.index,
            'timestamp': str(self.timestamp),
            'data': self.data,
            'hash': self.hash
        })
