# import socket
import threading
import time
import sys
from MyReliableUDPSocket import MyReliableUDPSocket, Packet


rdt_socket = MyReliableUDPSocket('localhost', 3001, 'localhost', 3000, False)
# rdt_socket = MyReliableUDPSocket('localhost', 3001, 'localhost', 3000)

rdt_socket.create()

if rdt_socket.listen_for_connection():
        print(f"connected to {rdt_socket.dest_addr}:{rdt_socket.dest_port} succesfully\n")


# start = time.time()
# while not rdt_socket.listen_for_connection():
#     print("listening for connection....")
#     if time.time()-start>10:
#         print("timeout")
        # exit()


req = rdt_socket.read()

print(req)

# rdt_socket.write('hello from server')

# print(rdt_socket.read())

