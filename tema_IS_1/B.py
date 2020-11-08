from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import binascii
import socket

host = '127.0.0.1'  # The server's hostname or IP address
portKM = 23456
portA = 65432
k=b'/\xa2\xa5\xb7t$"T\x82lR\x04j\x14w\xe5'
key=b''
IV=b"\xff\xc1\x99\xbf\xec\xdc\x951\xe7\xaf\x18'\xcb\xd1\x93\xf6"
cipher=AES.new(k,AES.MODE_ECB)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, portA))
    s.listen()
    conn, addr = s.accept()

    mode = conn.recv(1024)
    print(mode)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, portKM))
        sock.send(mode)
        key = cipher.decrypt(sock.recv(1024))
    sock.close()
s.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host,portA))
    s.send(b'Ready')
s.close()