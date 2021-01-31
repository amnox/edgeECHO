import docker
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')

def create_node(environment, networking_config):
    probe = docker_client.create_container(image='demo-probe',environment=environment,networking_config=networking_config)
    return probe

def clear_node(container_id):
    return ''