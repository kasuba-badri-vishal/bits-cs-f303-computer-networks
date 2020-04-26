import socket
import threading
import random
import time
import hashlib
import math

PACKET_SIZE = 8
TIMEOUT = 1
DATA = 0
ACK = 1
SYN = 2
SYNACK = 3
FIN = 3
PACKET_STUCT = ['Type', 'checksum', 'seq_num', 'num_packets', 'data']

class Packet:
    '''
    This class represents a packet and its attributes.
    Packet structure is
    "<Type>\r\n<seq_num>\r\n<num_packets>\r\n<checksum>\r\n\r\n<data>\r\n\r\n"
    '''
    def __init__(self, Type, seq_num, num_packets, data):
        self.Type = Type
        self.seq_num = seq_num
        self.num_packets = num_packets
        self.data = data
        self.checksum = self.calc_checksum()

    def get_string(self):
        '''
        This method uses the attributes of the current Packet object to form a string 
        that is to be sent through the socket.

        returns packet bytes
        '''
        self.content = f'''{self.Type}\r\n{self.seq_num}\r\n{self.num_packets}\r\n{self.checksum}\r\n\r\n{self.data}\r\n\r\n'''
        return bytes(self.content, 'utf-8')

    def calc_checksum(self):
        '''
        This method calculates checksum of the packet attributes using md5 hash algorithm.
        
        returns 16-byte hash value
        '''
        string = f'''{self.Type}\r\n{self.seq_num}\r\n{self.num_packets}\r\n\r\n{self.data}\r\n\r\n'''
        return hashlib.md5(string.encode('utf-8')).digest()

    @staticmethod
    def decode_pkt(pkt_string):
        '''
        This static method takes a packet string and forms a Packet object
        from the values present in that string. It also checks if the packet
        has errors using the checksum.

        returns tuple of Packet object and a boolean check.
        '''
        pkt_arr = pkt_string.decode().split("\r\n")
        if int(pkt_arr[0])==ACK:
            p = Packet(int(pkt_arr[0]), int(pkt_arr[1]), int(pkt_arr[2]), int(pkt_arr[5]))
        else:
            p = Packet(int(pkt_arr[0]), int(pkt_arr[1]), int(pkt_arr[2]), pkt_arr[5])
        
        c = f'{p.calc_checksum()}'
        check = False
        if c == pkt_arr[3]:
            check = True

        return (p, check)


class MyReliableUDPSocket:
    '''
    This class implements the reliable data transfer protocol using udp sockets.
    '''

    def __init__(self, src_addr = 'localhost', src_port = 3000, dest_addr = 'localhost', dest_port = 3001, verbose = True):
        self.src_addr = src_addr # source address 
        self.src_port = src_port # source port number 
        self.dest_addr = dest_addr # destination address 
        self.dest_port = dest_port  # destination port number 
        self.cur_seq = 0 # sequence number to be used for a new packet
        self.seq_list = dict() # a dictionary with unacked packet sequence numbers as keys and (Packet object, time created) tuple as values
        self.ready_to_read = False # boolean value which tells read() method that all packets are received.
        self.verbose = verbose # True value will print sent/received sequence numbers
        self.connected = False # connection status
        self.recv_buffer = [] # list of unordered packets received.
        self.recv_thread = threading.Thread(target = self.recv_t) # Thread which takes care of receiving packets.
        self.retransmit_thread = threading.Thread(target = self.check_and_retransmit) # Thread which takes care of packet retransmissions.
        # self.recv_thread.daemon = True
        # self.retransmit_thread.daemon = True

    def create(self):
        '''
        This method creates the udp socket and binds it to
        source address and source port.
        '''
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((self.src_addr, self.src_port))

    def read(self):
        '''
        This method waits for all packets to be received and uses the reconstruct_data()
        function to reconstruct the packets and extract data.

        returns reconstructed data string
        '''
        data = ''
        # if self.connected:
        while self.ready_to_read==False:
            pass

        data = self.reconstruct_data()
        self.recv_buffer = []
        self.ready_to_read = False
        return data

    def recv(self):
        '''
        This function starts the recv_thread and retransmit_thread
        '''
        self.recv_thread.start()
        self.retransmit_thread.start()

        # self.recv_thread.join()
        # self.retransmit_thread.join()
        # self.listen_for_connection()

    def recv_t(self):
        '''
        This function is the target of recv_thread. Until the connection is closed
        it receives packets, decodes them into Packet objects and does operations
        based on the packet Type.
        '''
        while self.connected:
            try:
                msg, addr = self.s.recvfrom(1024)
            except:
                break
            # print(msg, addr)
            pkt, check = Packet.decode_pkt(msg)
            # print(f'received packet\n{pkt}')
            if pkt.Type==DATA:
                if check:
                    self.send_ack(pkt.seq_num)
                    self.recv_buffer.append(pkt)
                    if self.verbose:
                        print(f"received packet {pkt.seq_num}/{pkt.num_packets}")
                    if len(self.recv_buffer)==pkt.num_packets:
                        self.ready_to_read = True
            elif pkt.Type==ACK:
                if check:
                    if self.verbose:
                        print(f"received ack {pkt.data}")
                    if self.seq_list.get(pkt.data)!=None:
                        del self.seq_list[pkt.data]

            elif pkt.Type==FIN:
                if self.verbose:
                    print("received fin1")
                    print("sent ack1")
                self.send_ack(pkt.seq_num)
                if self.socket_type=='server':
                    p = Packet(FIN, 0, 1, str(random.randint(1e7, 1e8)))
                    self.s.sendto(p.get_string(), (self.dest_addr, self.dest_port))
                    if self.verbose:
                        print("sent fin2")

                    while self.connected:
                        msg, addr = self.s.recvfrom(1024)
                        pkt, check = Packet.decode_pkt(msg)
                        # print("received synack", pkt)
                        if pkt.Type==ACK:
                            if self.verbose:
                                print("received ack2")
                            # time.sleep()
                            self.connected = False
                    # self.listen_for_connection()
                else:
                    time.sleep(10)
                    self.connected = False
                    
    def reconstruct_data(self, pkt_list = ""):
        '''
        This function uses the unordered packets in the recv_buffer,
        puts them in order of sequence numbers and concatenates data
        field in all packets to get the total data.
        
        returns data as string
        '''
        data = ""
        if pkt_list=="":
            sorted_list = sorted(self.recv_buffer, key = lambda p:p.seq_num)
            for p in sorted_list:
                data += p.data
        else:
            sorted_list = sorted(pkt_list, key = lambda p:p.seq_num)
            for p in sorted_list:
                data += p.data

        return data        

    def check_and_retransmit(self):
        '''
        This is the target function for retransmit_thread. Until the connection 
        is disconnected it checks if any packet in the seq_list (sent packets) is timed out
        and retransmits them.
        '''
        while self.connected:
            t = time.time()
            time.sleep(0.5)
            seq_dict = self.seq_list.copy()

            for seq_num in seq_dict.keys():
                if t - seq_dict[seq_num][1] >= TIMEOUT:
                    self.s.sendto(seq_dict[seq_num][0].get_string(), (self.dest_addr, self.dest_port))
                    if self.verbose:
                        print(f"retransmitting seq {seq_num}")
                    # self.seq_dict[seq_num][1] = t
                    # if self.seq_list.get(seq_num):
                    #     self.seq_list[seq_num][1] = t

    def send_ack(self, seq):
        '''
        This method creates a Packet object with packet Type as ACK,
        assigns sequence number of the packet to be acked as the ack number,
        and sends it to the destination.
        '''
        p = Packet(ACK, 0, 1, seq)
        self.s.sendto(p.get_string(), (self.dest_addr, self.dest_port))

    def create_connected_pkt(self):
        pkt = Packet(DATA, 0, 1, str(random.randint(1e7, 1e8)))
        return pkt

    def connect(self):
        '''
        This method is called from the client host. It initiates
        a connection with a server by
        1) sending SYN packet.
        2) receives SYNACK
        3) and sends ACK to server.

        Now the connection is established.
        '''
        self.socket_type = 'client'
        print(f"connecting to {self.dest_addr}:{self.dest_port}")
        self.connected = False 
        p = Packet(SYN, 0, 1, str(random.randint(1e7, 1e8)))
        self.s.sendto(p.get_string(), (self.dest_addr, self.dest_port))

        while not self.connected:
            msg, addr = self.s.recvfrom(1024)
            pkt, check = Packet.decode_pkt(msg)
            # print("received synack", pkt)
            if self.verbose:
                print("received synack")
            if pkt.Type==SYNACK:
                self.send_ack(int(pkt.seq_num + 1))
                self.connected = True
                self.recv()
        return self.connected

    def listen_for_connection(self):
        '''
        This method is called from the server host. It receives
        SYN packet sent by a client and sends back a SYNACK packet.
        Now it receives an ACK and connection is established.
        '''
        self.socket_type = 'server'
        print(f"listening for connection on {self.src_port}")
        self.connected = False 
        while not self.connected:
            msg, addr = self.s.recvfrom(1024)
            pkt, check = Packet.decode_pkt(msg)
            # print("received syn", pkt)
            if pkt.Type==SYN:
                if self.verbose:
                    print("received syn")
                p = Packet(SYNACK, 0, 1, int(pkt.seq_num)+1)
                self.s.sendto(p.get_string(), (self.dest_addr, self.dest_port))
                while not self.connected:
                    msg, addr = self.s.recvfrom(1024)
                    pkt, check = Packet.decode_pkt(msg)
                    if pkt.Type == ACK:
                        self.connected = True
                        self.recv()
        return self.connected

    def get_packets(self, data):
        '''
        This method takes data to be sent as input, breaks it into 
        pieces of size less than the PACKET_SIZE and creates a Packet
        object for each of the pieces. Each packet is assigned a sequence
        number in the order of the original data.

        returns a list of Packet objects.
        '''
        pkt_list = []
        num_packets = math.ceil(len(data)/PACKET_SIZE)
        for i in range(0, len(data), PACKET_SIZE):
            if i+PACKET_SIZE<len(data):
                pkt_list.append(Packet(DATA, self.cur_seq, num_packets, data[i: i+PACKET_SIZE]))
            else:
                pkt_list.append(Packet(DATA, self.cur_seq, num_packets, data[i:]))
            self.cur_seq += 1

        return pkt_list

    def write(self, data):
        '''
        This method takes data to be sent to destination host as input,
        uses get_packets() method to get list of packets formed from the original data
        and sends each packet to destination host in order of sequence numbers.
        It also saves each sequence number, packet objects and time in a dictionary (seq_list)
        '''
        pkt_list = self.get_packets(data)

        for i in range(len(pkt_list)):
            # print(f"sending packet {i+1}/{len(pkt_list)}\n{Packet.decode_pkt(pkt_list[i].get_string())}")
            if self.verbose:
                print(f"sending packet {i+1}/{len(pkt_list)} seq: {pkt_list[i].seq_num}")
            self.s.sendto(pkt_list[i].get_string(), (self.dest_addr, self.dest_port))

            self.seq_list[pkt_list[i].seq_num] = [pkt_list[i], time.time()]

    def close(self):
        '''
        This method initiates the closing of a socket. It is invoked form the client
        side of the socket. It first waits for all the sent packets to be acked and 
        sends a FIN packet to server. Further steps are handled by recv_thread.
        Once the recv_thread ends execution, the connection is closed.
        '''
        while len(self.seq_list)>0:
            pass
        print("close called")
        p = Packet(FIN, 0, 1, str(random.randint(1e7, 1e8)))
        if self.verbose:
            print("sent fin1")
        self.s.sendto(p.get_string(), (self.dest_addr, self.dest_port))

        self.recv_thread.join()
        self.retransmit_thread.join()
        print("exiting..")
        return self.connected
                                