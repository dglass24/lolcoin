from pybitcoin.privatekey import BitcoinPrivateKey

class LolcoinPrivateKey(BitcoinPrivateKey):
    _pubkeyhash_version_byte = 31

private_key = LolcoinPrivateKey()
print 'private key: {}'.format(private_key.to_wif())

public_key = private_key.public_key()
print 'public address: {}'.format(public_key.address())