import rsa
import binascii
mess = 'IMKT{5anta_give_me_good_primes_4_r5a}'
with open('public-key.pem', 'r') as fo:
    data_pub = fo.read()
    public = rsa.PublicKey.load_pkcs1_openssl_pem(data_pub)
    enc = rsa.encrypt(mess.encode('ascii'),public)
encrypt = int(binascii.hexlify(enc),16)
print(f'c: {encrypt}')




with open('private-key.pem', 'r') as fp:
    unbytes = binascii.unhexlify(hex(encrypt).split('x')[1])
    data_priv = fp.read()
    private = rsa.PrivateKey._load_pkcs1_pem(data_priv)
    dec = rsa.decrypt(unbytes, private).decode('ascii')

print(f'n: {private.n}')
print(f'e: {private.e}')
print(f'p: {private.p}')
print(f'q: {private.q}')
print(f'dec is: {dec}')