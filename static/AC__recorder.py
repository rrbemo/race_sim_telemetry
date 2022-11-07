import socket
import ctypes
import struct

UDP_IP = "127.0.0.1"
#UDP_IP = "" # Use this to listen to all incoming UDP traffic on that port.
UDP_PORT = 9996

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

# AC Handshake (https://docs.google.com/document/d/1KfkZiIluXZ6mMhLWfDX1qAGbvhGRC3ZUzjVIt5FQpp4/pub)
# https://pymotw.com/2/socket/binary.html
message = (ctypes.c_uint32(1), ctypes.c_uint32(1), ctypes.c_uint32(0))
packer = struct.Struct('III')
packed_data = packer.pack(*message)
sock.sendall(packed_data)
#sock.sendall(message)

with open("static/ACTestTelem.txt", "w") as telem_file:
    while True:
        udp_packet = sock.recv(2048)
        #packet = json.loads(repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\""))
        packet = udp_packet
        print(packet)
        telem_file.write("%s \n" % packet)
