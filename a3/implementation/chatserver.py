from MyReliableUDPSocket import MyReliableUDPSocket, Packet
import threading

# RDT SOCKET OBJECT
rdt_socket = MyReliableUDPSocket('localhost', 3000, verbose = False)
# rdt_socket = MyReliableUDPSocket('localhost', 3000)

# CREATES THE SOCKET AND BINDS IT TO THE ADDRESS, PORT
rdt_socket.create()

# THREAD FUNCTION TO READ FROM THE CLIENT SIMULTANEOUSLY WHILE WRITING.
def read_from_socket():
    while rdt_socket.connected:
        msg = rdt_socket.read()
        print("\n[CLIENT]:\n" + msg + "\n\n[SERVER]:")

# CONTINUE LISTENING FOR OTHER CONNECTIONS, AFTER ONE CONNECTION IS CLOSED.
while True:
    if rdt_socket.listen_for_connection():
        # WHEN THE CONNECTION IS ESTABLISHED READ THREAD IS STARTED.
        print(f"connected to {rdt_socket.dest_addr}:{rdt_socket.dest_port}")
        read_thread = threading.Thread(target=read_from_socket)
        read_thread.start()

        while rdt_socket.connected:
            msg = input("[SERVER]:\n") 
            print()

            rdt_socket.write(msg)

        print("connection closed")
