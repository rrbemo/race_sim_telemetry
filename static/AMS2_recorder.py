from pcars2.stream import PCarsStreamReceiver

class MyPCarsListener(object):
    def handlePacket(self, data):
        # You probably want to do something more exciting here
        # You probably also want to switch on data.packetType
        # See listings in packet.py for packet types and available fields for each
        print(data)


listener = MyPCarsListener()
stream = PCarsStreamReceiver()
stream.addListener(listener)
stream.run()

# import socket
# import ctypes
# import struct
#
# UDP_IP = ""
# #UDP_IP = "" # Use this to listen to all incoming UDP traffic on that port.
# UDP_PORT = 5606
#
# sock = socket.socket(socket.AF_INET,  # Internet
#                      socket.SOCK_DGRAM)  # UDP
# sock.bind((UDP_IP, UDP_PORT))
#
# with open("AMS2TestTelem.txt", "w") as telem_file:
#     while True:
#         udp_packet = sock.recv(1400)
#         #packet = json.loads(repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\""))
#         packet = udp_packet
#         print(packet)
#         telem_file.write("%s \n" % packet)
