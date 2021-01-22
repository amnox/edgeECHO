import socket 
import json, enum,time

message_count = 100000
probe_ip = "probe" 
probe_port = 12345

class ProbeMessage(enum.Enum):
   data = 1
   terminate = 2
   connection = 3

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

def form_message(data):
    print("".join(data))
    return json.loads("".join(data))

def wait_for_feedback(c):
    data = []
    byte = ''
    while True:
        byte = c.recv(1).decode('ascii')
        if(byte==";"):
            data = form_message(data)
            if(data['type']==3):
                print("Resuming Stream")
                break
            data = []
            continue
        data.append(byte ) 

def Main(): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((probe_ip, probe_port)) 
    print("socket binded to port", probe_port) 
    
    # put the socket into listening mode 
    s.listen(5) 
    print("Probe is listening") 
    # establish connection with client 
    c, addr = s.accept() 
    print('Connected to :', addr[0], ':', addr[1]) 

    c.send(create_message('probe','You are connected to probe',3))
    wait_for_feedback(c)
    for i in range(0,message_count):
        c.send(create_message('probe',i,'1'))
        print("Sent data")
        
    c.send(create_message('probe',1,2))
    print("All messages sent, terminating connection")
    time.sleep( 5 )
    s.close() 

if __name__ == '__main__': 
    Main()