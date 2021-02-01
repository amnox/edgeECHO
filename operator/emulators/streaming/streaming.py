# Import socket module 
import socket 
import json, enum, os


probe_ip = os.environ.get('probe_ip')
probe_port = int(os.environ.get('probe_port'))
stream_ip = os.environ.get('stream_ip')
stream_port = int(os.environ.get('stream_port'))
plain_stream = os.environ.get('plain_stream')

socket_message = {
        'sender':'stream',
        'type':None,
        'data':None
    }

def create_message(sender, m_data, m_type):
    data = socket_message
    data['sender'] = sender
    data['data'] = m_data
    data['type'] = m_type
    data = json.dumps(data)+';'
    return data.encode('ascii')

def unpack_message(data):
    #print("".join(data))
    return json.loads("".join(data))

def segementation():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((stream_ip, stream_port)) 
    print("Segmentaion binded to port", stream_port) 
    
    # put the socket into listening mode 
    s.listen(5) 
    print("Segementation is listening") 
    # establish connection with client 
    c, addr = s.accept() 
    return c
    
def forward_to_segmentation(seg, data):
    
    seg.send((json.dumps(data)+';').encode('ascii'))

def Main(): 
    probe_stream = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    probe_stream.connect((probe_ip,probe_port)) 
    seg = None
    if plain_stream=='True':
        print(probe_ip,probe_port,stream_ip,stream_port, plain_stream,type(plain_stream))
        probe_stream.send(create_message('streaming',1,3))
    else:
        print("waiting for segementation node")
        seg = segementation()
        probe_stream.send(create_message('streaming',1,3))
    data = []
    byte = ''
    while True:
        byte = probe_stream.recv(1).decode('ascii')
        if(byte==";"):
            data = unpack_message(data)
            if(data['type']==2):
                break
            if seg:
                data['sender'] = 'streaming'
                forward_to_segmentation(seg, data)
            data = []
            continue
        data.append(byte ) 
    probe_stream.close() 
    if(seg):
        data['sender'] = 'streaming'
        forward_to_segmentation(seg,data)
        seg.close()
if __name__ == '__main__': 
    Main() 