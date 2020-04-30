# import socket
from MyReliableUDPSocket import MyReliableUDPSocket, Packet


# rdt_socket = MyReliableUDPSocket('localhost', 3001, False)
rdt_socket = MyReliableUDPSocket('localhost', 3001)

rdt_socket.create()

while True:
    if rdt_socket.listen_for_connection():
        print(f"connected to {rdt_socket.dest_addr}:{rdt_socket.dest_port} succesfully\n")

        req = rdt_socket.read()

        print(req)

# start = time.time()
# while not rdt_socket.listen_for_connection():
#     print("listening for connection....")
#     if time.time()-start>10:
#         print("timeout")
        # exit()


# rdt_socket.write('hello from server')

# print(rdt_socket.read())

