# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# msg = bytes("hello", 'utf-8')

# s.sendto(msg, ('localhost', 3002))
from threading import Thread

v = False

def func():
    global v
    x = 0
    for i in range(10000000): x+=i
    v = True
    print("v thread:", v)

t1 = Thread(target = func)
t1.start()

while not v:pass

print(v)

