import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


while True:
    
    print(s.recvfrom(1024))