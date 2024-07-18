# Traffic Generation toolset

This toolset provides a simple mechanism to generate real-time traffic across a network without PCAP replays.

Traffic generators are deployed as containers. Each container runs an MQTT client, which subscribes to one or more topics on an MQTT broker shared by all traffic generator clients. When a traffic generator receives a message for its topic, it will perform the traffic generation action(s) describes in that message.

As an example:

```
decription: Describe the thing
service_type: web
service_host: web-client-2
action:
    type: get # HTTP GET
    targets: # list of destinations to hit
        - http://10.99.99.130 
        - http://10.66.66.130 
        - http://10.55.55.130 
    uri: /employees # URI added to the target above
    loop_for: 0 # loop settings; 0 means loop forever
    loop_delay: # by default, there is a delay between loops (measured in seconds)
        min: 2
        max: 10
        randomize_method: random
    create_thread: True # Tells the client to create a subprocess for the loop so additional actions can be performed while it runs
```

## Prerequisites

### Deployment device
- Ansible
- Terraform
- Python + required modules
- SSH + SUDO certificate-based login to all traffic generator hosts

### Wireless host(s)
- LXD
- One or more WiFi NICs

### Wired host(s)
- Docker

## Deployment Flows

### Wireless

The wireless clients are deployed as LXD containers. LXD was chosen for the flexibility of its low-level API. We take advantage of the ability to directly assign physical host interfaces to LXC namespaces so that we can create multiple WiFi clients on a single physical host by mapping WiFi NICs to unique containers.

1. Configure the Ansible inventory `inventory.yml`
2. Configure the `lxd_preseed.yml` file, which configures LXD settings on the traffic generator host
3. Run the `deploy_lxd.yml` playbook to deploy LXD and prerequisites to the LXD hosts
4. Run `build_netplan.py`. This script queries the LXD hosts, grabbing WiFi interface names and using them to generate the `main.tf` Terraform configuration file
5. Run `terraform apply` to build the WiFi clients.
6. Run `set_wifi_test.py` to configure the WiFi containers and authenticate
7. Run `start_wifis_tgen.py` to start traffic generator processes on WiFi containers

### Wired

1. Configure the Ansible inventory
2. Run the `prep_tg_clients.yml` playbook
3. Configure `tg_wired_vars.yml`
4. Run `build_assets.py`
5. Terraform apply

### Launch traffic generation

1. Define traffic generation parameters (defaults to file `tg_config.yml`)
2. Run `mqtt_test.py`