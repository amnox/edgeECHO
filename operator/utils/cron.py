import sqlite3, docker

client = docker.from_env()
DATABASE = '../database.db'
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
c = lambda a : client.containers.get(a)
n = lambda a : client.networks.get(a)

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def select_active_sessions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM session WHERE complete=?", (0,))

    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append(row)
    return results

def get_nodes(conn, session):
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes WHERE session_id=?", (session,))

    rows = cur.fetchall()
    results = []
    for row in rows:
        results.append(row[0])
    return results
def check_status(nodes):
    for n in nodes:
        if(c(n).status!='exited'):
            return False
    return True

def get_execution_time(node):
    ""
    state = c(node).attrs['State']
    start = state['StartedAt'].split('.')[0]+'.'+state['StartedAt'].split('.')[1][:5]+'Z'
    finish = state['FinishedAt'].split('.')[0]+'.'+state['FinishedAt'].split('.')[1][:5]+'Z'
    return [start,finish]

def update_tables(conn,session, nodes):
    session_sql = '''UPDATE session SET complete = ? WHERE session_id = ?'''
    node_sql = '''UPDATE nodes SET start = ? ,finish = ? ,status = ? WHERE node_id = ?'''
    cur = conn.cursor()
    cur.execute(session_sql, (1,session))
    for n in nodes:
        node_values = get_execution_time(n)
        node_values.extend(['exited',n])
        node_values = tuple(node_values)
        cur.execute(node_sql, node_values)
    conn.commit()

def cleanup(session, nodes):
    ""
    n(session[3]).remove()
    for node in nodes:
        c(node).remove()
def scheduled():
    """Run scheduled job."""
    print('Fetching sessions...')
    conn = create_connection(DATABASE)
    active_sessions = select_active_sessions(conn)
    for s in active_sessions:
        nodes = get_nodes(conn, s[0])
        if(check_status(nodes)):
            update_tables(conn,s[0],nodes)
            cleanup(s,nodes)
    print('Done!')

scheduled()
#get_execution_time('e88c8a1e964b1ba6283dfb187454349291abd3b5402de3368e7a9226dd6abd7f')