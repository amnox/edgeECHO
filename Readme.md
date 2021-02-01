# Operator Description

## Responsibilites

- Keep track of system resources

- Listen for incoming connections

- Make connections and wire things up

- Start and stop containers

## Workflows
_Note: Probe is a prerequisite for the following worflows_

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

Docker Python SDK: https://docker-py.readthedocs.io/en/stable/

# Setup

## Emulators

### Probe
```
cd /operator/emulators/probe/
docker build -t demo-probe .
```
### Streaming
```
cd /operator/emulators/streaming/
docker build -t demo-stream .
```
### Segmentation
```
cd /operator/emulators/segmentation/
docker build -t demo-segmentation .
```
### Test Connection
```
docker network create client_server_network

docker run --env probe_ip=probe --env probe_port=12345 --env count=100000 --network-alias probe --network client_server_network -it demo-probe

docker run --env probe_ip=probe --env probe_port=12345 --env stream_ip=stream --env stream_port=12346 --env plain_stream=False --network-alias stream --network client_server_network -it demo-stream

docker run --env stream_ip=stream --env stream_port=12346 --network client_server_network -it demo-segmentation
```

## Operator Server

```
cd operator/
python -m pip install -r req.txt
```


## Cron Jobs

Before proceeding with this section make sure you note the complete location of repository locally

```
crontab -e
```
Add this line at the end

```
* * * * * cd {Operator Server Location} && python utils/cron.py > /dev/null 2>&1
```

Save the changes and exit

**REST API REFERECE**

* **URL**
  http://127.0.0.1:5000/post/

* **Method:**
  
  `POST` 
  
*  **BODY**

   `JSON`

* **Data Params**

  `count` <Integer>
  `plain_stream` <Boolean>

* **Success Response:**


  * **Code:** 200 
    **Content:** `{'session_id': 'EE705B6538693C50', 'network': 'network_4B7EA', 'probe': 'a07fa236c7c646bb84cc622f240c3da044e6ede346baecaae1c2d8f95cd78f1e', 'stream': '5719c748397f95c6fb82270c60353107aa29aca09194c60fda11791e33660dc9', 'segmentation': '9ed19c932812985bd0870c9654dcb6d71b5acb1407016286553824e911704b44'}`
 

* **Sample Call:**

    ```
    import requests
    
    url = "http://127.0.0.1:5000/post/"
    
    payload="{\"count\": 100000,\"plain_stream\":false}\n"
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    print(response.text)
    
    ```