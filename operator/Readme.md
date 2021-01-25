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
