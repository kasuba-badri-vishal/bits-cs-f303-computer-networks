from MyReliableUDPSocket import MyReliableUDPSocket, Packet
import threading

# RDT SOCKET OBJECT
rdt_socket = MyReliableUDPSocket('localhost', 3001, verbose = False)
# rdt_socket = MyReliableUDPSocket('localhost', 3001)

# CREATES THE SOCKET AND BINDS IT TO THE ADDRESS, PORT
rdt_socket.create()

# THREAD FUNCTION TO READ FROM THE SERVER SIMULTANEOUSLY WHILE WRITING.
def read_from_socket():
    while rdt_socket.connected:
        msg = rdt_socket.read()
        print("\n[SERVER]:\n" + msg + "\n\n[CLIENT]:")


if rdt_socket.connect('localhost', 3000):
    # WHEN THE CONNECTION IS ESTABLISHED READ THREAD IS STARTED
    print(f"\nconnected to {rdt_socket.dest_addr}:{rdt_socket.dest_port}\n")
    read_thread = threading.Thread(target=read_from_socket)
    read_thread.start()

    while rdt_socket.connected:
        # PROMPT FOR WRITING MESSAGE. REPEATS UNTIL CONNECTION IS CLOSED
        msg = input("[CLIENT]:\n")
        print()
        rdt_socket.write(msg)