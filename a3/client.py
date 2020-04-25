# import socket
import threading
import time
from MyReliableUDPSocket import MyReliableUDPSocket, Packet

rdt_socket = MyReliableUDPSocket('localhost', 3000, 'localhost', 3001, False)
# rdt_socket = MyReliableUDPSocket('localhost', 3000, 'localhost', 3001)

rdt_socket.create()
if rdt_socket.connect():
    print(f"connected to {rdt_socket.dest_addr}:{rdt_socket.dest_port} succesfully")

print("\n")

rdt_socket.write('The Morgan Black Hours is an illuminated book of hours produced in Bruges between 1460 and 1480. It is one of seven surviving black books of hours, all originating from Bruges and dated to the mid- to late 15th century. They are named for their unusual dark blueish colourisation, achieved through the expensive process of dyeing the vellum with iron gall ink. The Morgan Black Hours consists of 121 leaves, most containing rows of Latin text written in Gothic minuscule script inscribed in silver and in gold. The pages are typically dyed a deep blueish black, with borders ornamented with flowers, foliage and grotesques. Although considered a masterpiece of Late Gothic manuscript illumination, there are no surviving records of its commission, but its dark tone, expense of production, quality and rarity suggest ownership by privileged and sophisticated members of the Burgundian court. It has been in the collection of the Morgan Library & Museum in New York since 1912.')
# rdt_socket.write('abcdefghijklmnopqrstuvwxyz')

# out = rdt_socket.read()

# print(out)

rdt_socket.write("ok bye")

rdt_socket.close()
