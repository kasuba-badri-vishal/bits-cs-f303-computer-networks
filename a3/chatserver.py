from MyReliableUDPSocket import MyReliableUDPSocket, Packet
import threading

rdt_socket = MyReliableUDPSocket('localhost', 3000, verbose = False)
# rdt_socket = MyReliableUDPSocket('localhost', 3000)

rdt_socket.create()

def read_from_socket():
    while rdt_socket.connected:
        msg = rdt_socket.read()
        print("\n[CLIENT]:\n" + msg + "\n\n[SERVER]:")

while True:
    if rdt_socket.listen_for_connection():
        print(f"connected to {rdt_socket.dest_addr}:{rdt_socket.dest_port}")
        read_thread = threading.Thread(target=read_from_socket)
        read_thread.start()

        while rdt_socket.connected:
            msg = input("[SERVER]:\n") 
            print()

            rdt_socket.write(msg)

        print("connection closed")