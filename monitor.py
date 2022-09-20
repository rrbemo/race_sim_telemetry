import socket
import json
import time
from packets import (
    PacketHeader,
    PacketID,
    HeaderFieldsToPacketType,
    unpack_udp_packet,
)

UDP_IP = "127.0.0.1"
UDP_PORT = 22022

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

data = [b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9\x0etZ<\x01\x00\x00\x00\x13\xffBUTN\x00\x00\x00\x00Z\x17-WZ\x17-W',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9\xab\x81\xce?O\x00\x00\x00\x13\xffSTLG\x02\n\x04\xab\x01\x00\x00\x00D\xd00B',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9\x06t\x1a@y\x00\x00\x00\x13\xffSTLG\x03\n\x04\xab\x01\x00\x00\x00D\xd00B',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9m\xda\x80@\xcc\x00\x00\x00\x13\xffSTLG\x05\n\x04\xab\x01\x00\x00\x00D\xd00B',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9\x8d\x99\xd9@\\\x01\x00\x00\x13\xffLGOT\xf0?5C\x01\x00\x00\x00\x00\x00\x00\x00',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9\x00\x00\x00\x00\x00\x00\x00\x00\x13\xffSSTA\x00\x00\x00\x97\x01\x00\x00\x00\x00\x00\x00\x10',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9+\xd0IA\x8a\x02\x00\x00\x13\xffSPTP\t\xc1\xe31C\x01\x01\t\xc1\xe31C',
        b'\xe6\x07\x01\x0b\x01\x03\xfd\xdeRL\xf9\xfa.\xa9o\x14NA\x98\x02\x00\x00\x13\xffSPTP\x0f\xab\xa5>C\x01\x01\x0f\xac\xa5>C',]
d = 0

while d < len(data):
    packet = json.loads(repr(unpack_udp_packet(data[d])).replace("\"", "").replace("'", "\""))
    #packet = repr(unpack_udp_packet(data[d])).replace("\"", "")
    print(packet["header"]["packetFormat"])
    d = d + 1

#with open("Telemetry_test.txt", "w") as telem_file:
#    while True:
#        telem_file.write("%s,\n" % sock.recv(2048))

#quitflag = False
#with open("TestTelem.txt", "w") as telem_file:
#    telem_file.write("This is the test Telem file for 09/18/2022 \n")
#    while not quitflag:
#        udp_packet = sock.recv(2048)
#        packet = unpack_udp_packet(udp_packet)
#        telem_file.write("%s \n" % repr(packet))

#while not quitflag:
#    udp_packet = sock.recv(2048)
#    packet = unpack_udp_packet(udp_packet)
#    print(packet.__dict__)
