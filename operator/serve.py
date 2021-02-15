import sqlite3
from flask import Flask, request
from datetime import datetime
from EdgeEchoSession import EdgeEchoSession
#import app
app = Flask(__name__)
DATABASE = 'database.db'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def insert_data(data):
    conn = create_connection(DATABASE)
    session_sql = '''INSERT INTO session (session_id,type,message_count,network,start_time) VALUES (?,?,?,?,?)'''
    nodes_sql = '''INSERT INTO nodes (node_id, session_id, start, finish, status, type) VALUES (?,?,?,?,?,?)'''
    
    d = datetime.now()
    session = (data['session_id'], data['stream_type'], data['message_count'], data["network"],d.strftime(DATE_FORMAT))
    probe_node = (data['probe'], data['session_id'], '','','running', "probe")
    stream_node = (data['stream'], data['session_id'], '','','running', "stream")
    segmentation_node = None
    if(data['segmentation']):
        segmentation_node = (data['segmentation'], data['session_id'], '','','running', "segmentation")
    
    cur = conn.cursor()
    cur.execute(session_sql, session)
    cur.execute(nodes_sql, probe_node)
    cur.execute(nodes_sql, stream_node)
    if(segmentation_node):
        cur.execute(nodes_sql, segmentation_node)
    conn.commit()


@app.route('/',methods=['GET'])
def hello_world():
    return 'Hello World'
@app.route('/test', methods=['GET'])
def test_route():
    return "Working"

@app.route('/post/',methods=['POST'])
def show_post():
    r = request.get_json()
    count, plain_stream = r['count'], r['plain_stream']
    edge_echo_session = EdgeEchoSession(count, plain_stream)
    nodes = edge_echo_session.create_session()
    edge_echo_session.start_seassion()
    print(nodes)
    nodes['message_count'] = count
    nodes['stream_type'] = "plain" if plain_stream else "segmented"
    insert_data(nodes)
    return nodes

