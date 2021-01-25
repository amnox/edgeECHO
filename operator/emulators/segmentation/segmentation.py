# Import socket module 
import socket 
import json, enum, os

stream_ip = os.environ.get('stream_ip')
stream_port = int(os.environ.get('stream_port'))

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
    print("".join(data))
    return json.loads("".join(data))

def Main(): 
    stream_seg = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    stream_seg.connect((stream_ip,stream_port)) 
    #stream_seg.send(create_message('streaming',1,3))

    data = []
    byte = ''
    while True:
        byte = stream_seg.recv(1).decode('ascii')
        if(byte==";"):
            data = unpack_message(data)
            if(data['type']==2):
                break
            data = []
            continue
        data.append(byte ) 
    stream_seg.close() 

if __name__ == '__main__': 
    Main() 