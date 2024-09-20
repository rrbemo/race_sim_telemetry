import socket
import json
from packets_f123 import (
    unpack_udp_packet,
)

#UDP_IP = "127.0.0.1"
UDP_IP = "" # Use this to listen to all incoming UDP traffic on that port.
UDP_PORT = 22023

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

with open("static/TestTelem.txt", "w") as telem_file:
    while True:
        udp_packet = sock.recv(2048)
        #packet = json.loads(repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\""))
        packet = repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\"")
        telem_file.write("%s \n" % packet)
