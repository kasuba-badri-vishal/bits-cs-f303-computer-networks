TEAM MEMBERS
Raj Kashyap Mallala	      2017A7PS0025H
S Rohith                      2017A7PS0034H
T Naga Sai Bharath    	      2017A7PS0209H
Kasuba Badri Vishal   	      2017A7PS0270H
Nimmagadda Bhargav 	      2017A7PS01574H


In this assignment a reliable appplication layer protocol has been implemented using udp sockets.

Language used: python
modules used: socket, threading, time, hashlib, random, time

The file MyReliableUDPSocket.py contains

1) Packet class - defines packet structure, decodes a string into Packet object and encodes it into 
                    a string which can be sent through socket.

2) MyReliableUDPSocket - implements the reliable layer on top of udp sockets.
                       - an application can use its write method to send a message/string
                         to a specified destination.
                       - It uses read method to get received string from recv_buffer.
                       - The read method uses reconstruct_data method to correctly reorder received packets.
                       - multithreading has been used to simulataneously receive incoming packets into a recv recv_buffer
                         and also do other operations like sending packets, retransmitting packets etc.


TOY APPLICATION:
   
    - a chat application has been created using the MyReliableUDPSocket. In this application, two users
      can chat with each other by typing in the terminal. 
   
    - Users can simulataneously send and receive messages, because the read 
      function runs on a different thread.

    - the files chatserver.py and chatclient.py implement this chat application


STEPS TO RUN:

    - python chatserver.py
        1. The server listens for connection from any addr,port..
        2. When a client initiates connection, it is connected to the client
            and chatting can be started

    - python chatclient.py
        1. connects to a specified server (addr, port).
        2. retries the connection three times and exits if cannot connect.
        3. if the server is online, it connects to it and chatting can be started.