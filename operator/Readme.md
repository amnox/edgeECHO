Operator Description

Responsibilites

- Keep track of system resources
- Listen for incoming connections
- Make connections and wire things up
- Start and stop containers

Workflows
Prerequisite - Probe

- Normal stream request
-- Get probe details
-- Start a streaming server
-- Return the location to requester
- Segmented Stream Request
-- Get probe details
-- Start a streaming server
-- Start Segmentation Server


Python Env Variables: https://www.nylas.com/blog/making-use-of-environment-variables-in-python/
Docker env variables: https://docs.docker.com/compose/environment-variables/#set-environment-variables-in-containers
Stream needs to know Probe IP
Seg needs to know Stream IP

Python SDK

- Start a container




docker run --env probe_ip=probe --env probe_port=12345 --env count=100000 --network-alias probe --network client_server_network -it demo-probe

docker run --env probe_ip=probe --env probe_port=12345 --env stream_ip=stream --env stream_port=12346 --env plain_stream=True --network-alias stream --network client_server_network -it demo-stream

docker run --env stream_ip=stream --env stream_port=12346 --network client_server_network -it demo-segmentation



e = {"probe_ip": "probe","probe_port": "12345","count": 100000}

f = {"probe_ip": "probe","probe_port": "12345","stream_ip":"0.0.0.0","stream_port":12346,"plain_stream":True}

client = docker.from_env()

probe = client.containers.create("demo-probe",environment=e, hostname="probe",network_mode="client_server_network")

stream = client.containers.create("demo-stream",environment=f)


network = client.networks.create("client_server_network", driver="bridge",attachable=True,check_duplicate=True)

network.connect(probe,aliases=['probe'])


import docker
client = docker.from_env()
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
sn = lambda a : str(client.networks.list())

sc = lambda a : client.containers.list()

pn = lambda a :client.networks.prune()

pc = lambda a :client.containers.prune()

c = lambda a : client.containers.get(a)

n = lambda a : client.networks.get(a)


networking_config = docker_client.create_networking_config({
                'client_server_network': docker_client.create_endpoint_config(
                    aliases=['probe'],
                )
            })
'client_server_network': {'IPAMConfig': None, 'Links': None, 'Aliases': ['probe', '543c853a0000'], 'NetworkID': '16acea2b8f378b820e7d794eabea5cbec7076cdf2e3fc9f09b0a082be308ffb8', 'EndpointID': 'a13020589d57a8611de095dd772b3515edd556e4262d14a6258317099a9a3a70', 'Gateway': '192.168.224.1', 'IPAddress': '192.168.224.2', 'IPPrefixLen': 20, 'IPv6Gateway': '', 'GlobalIPv6Address': '', 'GlobalIPv6PrefixLen': 0, 'MacAddress': '02:42:c0:a8:e0:02', 'DriverOpts': None}}


networking_config = docker_client.create_networking_config({'client_server_network': docker_client.create_endpoint_config(aliases=['probe'])})

probeme = docker_client.create_container(image='demo-probe',environment=e,networking_config=networking_config)

docker_client.start(probeme)

