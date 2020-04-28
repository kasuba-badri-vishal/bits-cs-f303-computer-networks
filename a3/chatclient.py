from MyReliableUDPSocket import MyReliableUDPSocket, Packet
import threading

# rdt_socket = MyReliableUDPSocket('localhost', 3001, verbose = False)
rdt_socket = MyReliableUDPSocket('localhost', 3001)

rdt_socket.create()

def read_from_socket():

    while True:
        msg = rdt_socket.read()
        print("\nServer: ", msg, "\nClient: ")

if rdt_socket.connect('localhost', 3000):
    print(f"\nconnected to {rdt_socket.dest_addr}:{rdt_socket.dest_port}\n")
    read_thread = threading.Thread(target=read_from_socket)
    read_thread.start()


while rdt_socket.connected:

    msg = input("\nClient: ")

    rdt_socket.write(msg)

    # recv_msg = rdt_socket.read()

    # print("Server:", recv_msg)