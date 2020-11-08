from Cryptodome.Cipher import AES
import socket
from _thread import *
import threading

print_lock = threading.Lock()
k_CBC=b'\x8d\x00\x0c\xa1\x87\xc48\xf3\xe7\xbb\x06\x83\xa3(\x17\x17'
k_OFB=b'\x1b1\xae\x03C\x96\x9dw\xdd\xe2m$\x18|\xb1Z'
k=b'/\xa2\xa5\xb7t$"T\x82lR\x04j\x14w\xe5'

# thread function
def threaded(c):
    while True:

        cipher = AES.new(k, AES.MODE_ECB)
        # data received from client 
        data = c.recv(1024)
        print(data)
        if not data:
            print('Bye')

            # lock released on exit 
            print_lock.release()
            break

        # reverse the given string from client 
        if data.decode("utf-8")=='CBC':
            print(cipher.encrypt(k_CBC))
            c.send(cipher.encrypt(k_CBC))
        elif data.decode("utf-8")=='OFB':
            c.send(cipher.encrypt(k_OFB))

        # send back reversed string to client 


        # connection closed
    c.close()


def Main():
    host = '127.0.0.1'

    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 23456
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode 
    s.listen(10)
    print("socket is listening")

    # a forever loop until client wants to exit 
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client 
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,))
    s.close()

if __name__ == '__main__':
    Main()

