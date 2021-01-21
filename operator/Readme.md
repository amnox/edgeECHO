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



docker network create client_server_network
docker run --network-alias server --network client_server_network -it amnox/probe_emulator:1.1
docker run --network client_server_network -it amnox/streaming:1.1