import ecdsa
import hashlib
from hashlib import sha256
import struct

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

class Wallet(object):
    def __init__(self):
        pass

    def generate(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).to_string().encode('hex')
        self.private_key_wif = self.privateKeyToWif(self.private_key)
        self.public_key = self.privateKeyToPublicKey(self.private_key)
        self.address = self.keyToAddr(self.private_key)

    def verify(self, address):
        return self.check_bc(address)

    def decode_base58(self, bc, length):
        n = 0
        for char in bc:
            n = n * 58 + digits58.index(char)
        return ('%%0%dx' % (length << 1) % n).decode('hex')[-length:]

    def check_bc(self, bc):
        bcbytes = self.decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]

    # Returns byte string value, not hex string
    def varint(self, n):
        if n < 0xfd:
            return struct.pack('<B', n)
        elif n < 0xffff:
            return struct.pack('<cH', '\xfd', n)
        elif n < 0xffffffff:
            return struct.pack('<cL', '\xfe', n)
        else:
            return struct.pack('<cQ', '\xff', n)

    # Takes and returns byte string value, not hex string
    def varstr(self, s):
        return self.varint(len(s)) + s

    # 60002
    def netaddr(self, ipaddr, port):
        services = 1
        return (struct.pack('<Q12s', services, '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff') +
                           struct.pack('>4sH', ipaddr, port))

    # return value, len
    def processVarInt(self, payload):
        n0 = ord(payload[0])
        if n0 < 0xfd:
            return [n0, 1]
        elif n0 == 0xfd:
            return [struct.unpack('<H', payload[1:3])[0], 3]
        elif n0 == 0xfe:
            return [struct.unpack('<L', payload[1:5])[0], 5]
        else:
            return [struct.unpack('<Q', payload[1:5])[0], 7]

    # return value, len
    def processVarStr(self, payload):
        n, length = self.processVarInt(payload)
        return [payload[length:length+n], length + n]

    # takes 26 byte input, returns string
    def processAddr(self, payload):
        assert(len(payload) >= 26)
        return '%d.%d.%d.%d:%d' % (ord(payload[20]), ord(payload[21]),
                                   ord(payload[22]), ord(payload[23]),
                                   struct.unpack('!H', payload[24:26])[0])

    def base58encode(self, n):
        result = ''
        while n > 0:
            result = b58[n%58] + result
            n /= 58
        return result

    def base58decode(self, s):
        result = 0
        for i in range(0, len(s)):
            result = result * 58 + b58.index(s[i])
        return result

    def base256encode(self, n):
        result = ''
        while n > 0:
            result = chr(n % 256) + result
            n /= 256
        return result

    def base256decode(self, s):
        result = 0
        for c in s:
            result = result * 256 + ord(c)
        return result

    def countLeadingChars(self, s, ch):
        count = 0
        for c in s:
            if c == ch:
                count += 1
            else:
                break
        return count

    # https://en.bitcoin.it/wiki/Base58Check_encoding
    def base58CheckEncode(self, version, payload):
        s = chr(version) + payload
        checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
        result = s + checksum
        leadingZeros = self.countLeadingChars(result, '\0')
        return '1' * leadingZeros + self.base58encode(self.base256decode(result))

    def base58CheckDecode(self, s):
        leadingOnes = self.countLeadingChars(s, '1')
        s = self.base256encode(self.base58decode(s))
        result = '\0' * leadingOnes + s[:-4]
        chk = s[-4:]
        checksum = hashlib.sha256(hashlib.sha256(result).digest()).digest()[0:4]
        assert(chk == checksum)
        version = result[0]
        return result[1:]

    def privateKeyToWif(self, key_hex):
        return self.base58CheckEncode(0x80, key_hex.decode('hex'))

    def privateKeyToPublicKey(self, s):
        sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        return (sk.verifying_key.to_string()).encode('hex')
        #return ('\80' + sk.verifying_key.to_string()).encode('hex')

    def pubKeyToAddr(self, s):
        ripemd160 = hashlib.new('ripemd160')
        ripemd160.update(hashlib.sha256(s.decode('hex')).digest())
        return self.base58CheckEncode(0, ripemd160.digest())

    def keyToAddr(self, s):
        return self.pubKeyToAddr(self.privateKeyToPublicKey(s))

wallet = Wallet()
wallet.generate()

print 'private key:\t\t{}'.format(wallet.private_key)
print 'private key wif:\t\t{}'.format(wallet.private_key_wif)
print 'public key:\t\t{}'.format(wallet.public_key)
print 'wallet:\t\t{}'.format(wallet.address)

print wallet.verify(wallet.address)