from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import socket
import threading
import json
from simstore.simstore import SimStore
import simdataclasses.simdataclasses as rsdc
from packets.packets_f123 import (
    unpack_udp_packet,
    PacketID
)
import yaml

app = Flask(__name__)

# TODO: find a way to handle more packets... listener sends to a different thread?
# Maybe spawn a thread to handle each type of packet?
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
        # This is fairly fast and seems to allow a lot of data to be stored.
        my_connection.execute_query(f"INSERT INTO raw_packet (json_data) VALUES (%s)", (packet,))

        # Start a thread to process this packet.
        # threading.Thread(target=process_packet, args=(my_connection, packet,), daemon=True).start()
        # Or, just run the function without a thread
        process_packet(my_connection, packet)

def process_packet(conn, packet):
    # Now parse and save the packet into their own tables.
    # This is likely much slower and takes more time to save.
    json_packet = json.loads(packet)
    data = []
    if json_packet:
        if json_packet['header']:
            packet_id = json_packet['header']['packetId']
            print("Packet: " + packet_id)

            # TODO: is it possible to start new threads to process and save each packet?
            # If so, at this point, maybe the rsdc class should have a packet handler
            # That funtion should be called for each packet and it should save to the database as needed.
            match packet_id:
                case '1':
                    data = rsdc.SessionDetails.packet_to_data(json_packet)
                case '2':
                    data = rsdc.LapData.packet_to_data(json_packet)
                case '4':
                    # This packet only seems to be created for online lobbies.
                    data = rsdc.SessionParticipant.packet_to_data(json_packet)
                case '6':
                    data = rsdc.Telemetry.packet_to_data(json_packet)
                case '7':
                    data = rsdc.CarStatusData.packet_to_data(json_packet)
                case '8':
                    print('Attempting to handle outcome packet!')
                    data = rsdc.SessionOutcome.packet_to_data(json_packet)
                    data = data + rsdc.SessionTyreStint.packet_to_data(json_packet) # non-nested way to add list items
                case _:
                    #print("packet not handled " + packet_id + " :: " + PacketID(int(packet_id)).name)
                    pass

    if data:
        for d in data:
            print(d)
            # Execute an insert for each data object
            conn.execute_query(d.insert_string())

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

@app.route("/sessions")
def show_sessions():
    # Get all unique sessions and some helpful data to make a selection
    my_connection = SimStore()
    sessions = my_connection.execute_query("SELECT DISTINCT session_uid FROM car_telemetry")

    template_data = sessions

    return render_template('session_selector.html', **template_data)


@app.route("/session/<int:session_id>")
def show_session_data(session_id):
    # Get some session data
    my_connection = SimStore()
    session_data = my_connection.execute_query(f"SELECT ct.*, "
                                               f"sp.driver_name "
                                               f"FROM car_telemetry ct "
                                               f"LEFT JOIN session_participant sp ON ct.session_uid = sp.session_uid "
                                               f"  AND ct.participant_index = sp.participant_index "
                                               f"WHERE ct.session_uid = '{session_id}'")

    print(session_data)

    session_data['driver_name'] = session_data['driver_name'].fillna('')

    # Display a something
    template_data = session_data.groupby(['participant_index', 'driver_name'])

    # build a plot
    visual = px.line(session_data, title='Throttle', x='session_time', y='throttle', color='participant_index')
    vis = visual.to_html(full_html=False)
    return render_template('session_details.html', data=template_data, vis=vis)

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=8080)#debug=True, threaded=True)