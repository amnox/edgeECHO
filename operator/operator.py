import pymongo, sqlite3
from flask import Flask, request, g
from EdgeEchoSession import EdgeEchoSession
app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/',methods=['GET'])
def hello_world():
    return 'Hello World'

@app.route('/post/',methods=['POST'])
def show_post():
    # show the post with the given id, the id is an integer
    r = request.get_json()
    count, plain_stream = r['count'], r['plain_stream']
    edge_echo_session = EdgeEchoSession(count, plain_stream)
    nodes = edge_echo_session.create_session()
    edge_echo_session.start_seassion()
    print(nodes)
    return nodes
if __name__ == '__main__':
    app.run(debug = True)