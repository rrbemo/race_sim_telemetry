import socket
import struct
import time
from .packets import (
    PacketHeader,
    PacketID,
    HeaderFieldsToPacketType,
    unpack_udp_packet,
)


from collections import namedtuple

TimestampedPacket = namedtuple("TimestampedPacket", "timestamp, packet")


#sock = socket.socket(socket.AF_INET, # Internet
#                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))

data = "b'\xe6\x07\x01\t\x01\x03`\xb9\xdeM\xff)\xfe\xebN\x826C\x18(\x00\x00\x00\xffBUTN\x10\x08\x00\x00Z\x17-WZ\x17-W'"
quitflag = False
while not quitflag:
    timestamp = time.time()

    # All telemetry UDP packets fit in 2048 bytes with room to spare.
    packet = sock.recv(2048)
    timestamped_packet = TimestampedPacket(timestamp, packet)

#while True:
    #data, addr = sock.recvfrom(2*1024) # buffer size is 1024 bytes

    #print("received message: %s" % print_data)