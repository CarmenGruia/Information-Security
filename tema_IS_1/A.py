from Cryptodome.Cipher import AES

import socket

from Cryptodome.Util.Padding import pad


def bxor(b1, b2): # use xor for bytes
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return result
host = '127.0.0.1'  # Standard loopback interface address (localhost)
portKM = 23456
portB = 65432
mode_name = input("Mode ")
CBC=b'CBC'
OFB=b'OFB'
k=b'/\xa2\xa5\xb7t$"T\x82lR\x04j\x14w\xe5'
key=b''
IV=b"\xff\xc1\x99\xbf\xec\xdc\x951\xe7\xaf\x18'\xcb\xd1\x93\xf6"
cipher=AES.new(k,AES.MODE_ECB)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, portB))
    print(mode_name)
    if mode_name == 'CBC':
        s.send(CBC)
    elif mode_name == 'OFB':
        s.send(OFB)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, portKM))
        if mode_name == 'CBC':
            sock.send(CBC)
        elif mode_name == 'OFB':
            sock.send(OFB)
        key=cipher.decrypt(sock.recv(1024))
    sock.close()
s.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, portB))
    s.listen()
    conn, addr = s.accept()

    message = conn.recv(1024).decode('utf-8')
    print(message)
    print()
    if message!='Ready':
        breakpoint()
    elif message=='Ready':
        if mode_name=='CBC':
            f= open("text.txt")
            c=f.read()
            count=1
            c=str.encode(c)
            for plaintext in [c[i:i + 32] for i in range(0, len(c), 32)]:
                if count==1:
                    cipher = AES.new(k, AES.MODE_ECB)
                    plaintext=pad(plaintext, 16)
                    blockcipher=bxor(plaintext,IV)
                    count=0
                    ciphertext=cipher.encrypt(blockcipher)
                    print(ciphertext)
                else:
                    cipher = AES.new(k, AES.MODE_ECB)
                    plaintext = pad(plaintext, 16)
                    blockcipher=bxor(plaintext,ciphertext)
                    ciphertext=cipher.encrypt(blockcipher)
                    print(ciphertext)
        elif mode_name=='OFB':
            f = open("text.txt")
            c = f.read()
            count = 1
            c = str.encode(c)
            for plaintext in [c[i:i + 32] for i in range(0, len(c), 32)]:
                if count == 1:
                    cipher = AES.new(k, AES.MODE_ECB)
                    count=0
                    blockcipher=cipher.encrypt(IV)
                    plaintext = pad(plaintext, 16)
                    ciphertext=bxor(plaintext,blockcipher)
                    print(ciphertext)
                else :
                    cipher = AES.new(k, AES.MODE_ECB)
                    blockcipher = cipher.encrypt(blockcipher)
                    plaintext = pad(plaintext, 16)
                    ciphertext = bxor(plaintext, blockcipher)
                    print(ciphertext)









s.close()
