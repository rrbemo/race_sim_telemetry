from flask import Flask, Response, request, render_template, stream_with_context
import socket
import json
import time
from static.packets import (
    unpack_udp_packet,
)

app = Flask(__name__)

#UDP_IP = "127.0.0.1"
UDP_IP = "" # Use this to listen to all UDP traffic on that port.
UDP_PORT = 22022

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

@app.route("/")
def index():
    return render_template("test_view.html")

@app.route("/test_data")
def test_data():
    def listen_for_data():
        with open("static/TestTelem.txt", "w") as telem_file:
            #telem_file.write("This is the test Telem file for 09/18/2022 \n")
            while True:
                udp_packet = sock.recv(2048)
                packet = json.loads(repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\""))
                # Use this to write all data
                # telem_file.write("%s \n" % repr(packet))

                # Or filter by something in the header to save it off
                if (packet["header"]["packetId"] == "6"):
                    telem_file.write("%s \n" % repr(packet))
                    yield f"data:{json.dumps(packet)}\n\n"
                    time.sleep(0.1)

    response = Response(stream_with_context(listen_for_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response
    # data = {''}
    # return render_template('test_view.html', )

if __name__ == '__main__':
    app.run()#debug=True, threaded=True)