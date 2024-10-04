from flask import Flask, render_template
import pandas as pd
import socket
import threading
import psycopg2
import json
from packets.packets_f123 import (
    unpack_udp_packet,
)
import yaml

app = Flask(__name__)

# open the yaml file and read in the values
with open('static/config.yaml', 'r') as conf:
    db_conf = yaml.safe_load(conf)
usr = db_conf['db']['username']
pwd = db_conf['db']['pass']
host = db_conf['db']['host']
db_name = db_conf['db']['dbname']
table_name = db_conf['db']['tablename']


def udp_listener():
    # UDP_IP = "127.0.0.1"
    UDP_IP = ""  # Use "" to listen to all incoming UDP traffic on that port.
    UDP_PORT = 22023

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        database=db_name,
        user=usr,
        password=pwd
    )
    cur = conn.cursor()

    while True:
        udp_packet = sock.recv(2048)

        unpacked_packet = repr(unpack_udp_packet(udp_packet)).replace("\"", "").replace("'", "\"")
        try:
            # Do the conversion just to check that it is json convertable...
            json_packet = json.loads(unpacked_packet)
            #if (json_packet['header']['packetId'] in ("4", "10")):
            #    print(json_packet)

            # Write to db (use the non-dictionary, string version of the data)
            cur.execute(
               f"INSERT INTO {table_name} (json_data) VALUES (%s)", (unpacked_packet,))
            conn.commit()

            print(f"received and stored a packet from: somewhere")
        except ValueError:
            print(f"Unable to parse: {unpacked_packet}")


    cur.close()
    conn.close()

@app.route("/")
def index():
    message = "Race Sim says, Hello!"
    templateData = {"message": message}

    return render_template('index.html', **templateData)
@app.route("/packets", methods=['GET'])
def get_packets():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=host,
            database=db_name,
            user=usr,
            password=pwd
        )
        cur = conn.cursor()

        cur.execute(f"SELECT distinct json_data->'header'->>'sessionUID' as sessionUID FROM {table_name}")
        packet_data = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        return None

    column_names = ['sessionUID']
    df = pd.DataFrame(packet_data, columns=column_names)
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