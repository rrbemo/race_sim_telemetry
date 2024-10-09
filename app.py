from flask import Flask, render_template
import pandas as pd
import socket
import threading
import json
from simstore.simstore import SimStore
import simdataclasses.simdataclasses as rsdc
from packets.packets_f123 import (
    unpack_udp_packet,
)
import yaml

app = Flask(__name__)




def udp_listener():
    ## UDP listening
    # UDP_IP = "127.0.0.1"
    UDP_IP = ""  # Use "" to listen to all incoming UDP traffic on that port.
    UDP_PORT = 22023
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    ## Connection to database for saving
    my_connection = SimStore()
    while True:
        udp_packet = sock.recv(2048)

        packet = repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\"")
        # Save the raw packet like I originally was...
        my_connection.execute_query(f"INSERT INTO raw_packet (json_data) VALUES (%s)", (packet,))

        # Now parse and save the packet into their own tables.
        json_packet = json.loads(packet)
        data = None
        if json_packet:
            if json_packet['header']:
                match json_packet['header']['packetId']:
                    case '4':
                        # This packet only seems to be created for online lobbies.
                        data = rsdc.SessionParticipant.packet_to_data(json_packet)
                    case '6':
                        data = rsdc.Telemetry.packet_to_data(json_packet)
                    case '7':
                        # TODO: build a dataclass for the car damage packet
                        print("Missed a damage packet")
                    case '8':
                        # TODO: build a dataclass for the session outcome packet
                        print("Missed the outcomes packet")
                    case _:
                        print("packet not handled")

        if data:
            for d in data:
                # Execute an insert for each data object
                my_connection.execute_query(d.insert_string())

@app.route("/")
def index():
    message = "Race Sim says, Hello!"
    templateData = {"message": message}

    return render_template('index.html', **templateData)

@app.route("/packets", methods=['GET'])
def get_packets():
    unique_sessions = SimStore.execute_query(f"SELECT distinct json_data->'header'->>'sessionUID' as sessionUID FROM raw_packet")

    column_names = ['sessionUID']
    df = pd.DataFrame(unique_sessions, columns=column_names)
    print(df['sessionUID'])
    templateData = {
        "packets": [{'sessionUID': df['sessionUID']}]
    }
    return render_template("packet_view.html", **templateData)

@app.route("/session/<int:session_id>")
def show_session_data(session_id):
    pass

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)#debug=True, threaded=True)