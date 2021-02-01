import random, docker

class EdgeEchoSession:
    def __init__(self, count, plain_stream):
        self.session_id = self.__generate_id(16,'alpha')
        self.count = count
        self.plain_stream = plain_stream
        self.network = None
        self.probe = None
        self.stream = None
        self.segmentation = None
        self.client = docker.from_env()
        self.docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
    
    def __generate_id(self, length, id_type = 'alpha'):
        alpha_numeric = '0123456789ABCDEF'
        numeric = '123456'
        if(id_type=='alpha'):
            return ''.join(random.choice(alpha_numeric) for i in range(length))
        if(id_type=='num'):
            return int(''.join(random.choice(numeric) for i in range(length-1)))
    
    def create_probe(self,network, probe_ip,probe_port,count):
        environment = {"probe_ip": probe_ip,"probe_port": probe_port,"count": count}
        docker_client,network_dict = self.docker_client, {}
        network_dict[network] = docker_client.create_endpoint_config(aliases=[probe_ip])
        networking_config = docker_client.create_networking_config(network_dict)
        self.probe = docker_client.create_container(image='demo-probe',environment=environment,networking_config=networking_config)
        return self.probe

    def create_stream(self, network, probe_ip, probe_port, stream_ip, stream_port, plain_stream):
        environment = {"probe_ip": probe_ip,"probe_port": probe_port,"stream_ip":stream_ip,"stream_port":stream_port,"plain_stream":plain_stream}
        docker_client,network_dict = self.docker_client, {}
        network_dict[network] = docker_client.create_endpoint_config(aliases=[stream_ip])
        networking_config = docker_client.create_networking_config(network_dict)
        self.stream = docker_client.create_container(image='demo-stream',environment=environment,networking_config=networking_config)
        return self.stream

    def create_segmentaion(self, network, stream_ip, stream_port):
        environment = {"stream_ip":stream_ip,"stream_port":stream_port}
        docker_client,network_dict = self.docker_client, {}
        network_dict[network] = docker_client.create_endpoint_config()
        networking_config = docker_client.create_networking_config(network_dict)
        self.segmentation = docker_client.create_container(image='demo-segmentation',environment=environment,networking_config=networking_config)
        return self.segmentation

    def create_network(self):
        name = 'network_'+self.__generate_id(5,'alpha')
        network = self.client.networks.create(name, driver="bridge",attachable=True,check_duplicate=True)
        self.network = network
        return name

    def create_session(self):
        probe_name, probe_port = 'probe_'+self.__generate_id(5,'alpha'), self.__generate_id(5,'num')
        stream_name, stream_port = 'stream_'+self.__generate_id(5,'alpha'), self.__generate_id(5,'num')
        segmentation=None
        network = self.create_network()
        probe = self.create_probe(network,probe_name,probe_port,self.count)
        stream = self.create_stream(network,probe_name,probe_port,stream_name, stream_port, self.plain_stream)
        if(self.plain_stream==False):
            segmentation = self.create_segmentaion(network, stream_name,stream_port)
        return {
            'session_id':self.session_id,
            'network': network,
            'probe': probe['Id'],
            'stream': stream['Id'],
            'segmentation': segmentation['Id'] if (segmentation) else None
        }
    def start_seassion(self):
        docker_client = self.docker_client
        docker_client.start(self.probe['Id'])
        docker_client.start(self.stream['Id'])
        if(self.segmentation):
            docker_client.start(self.segmentation['Id'])
