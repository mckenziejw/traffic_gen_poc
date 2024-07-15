# Traffic Generation toolset

This toolset provides a simple mechanism to generate real-time traffic across a network without PCAP replays.

There are two sets of clients for wired and wireless connections respectively.

## Deployment (Wireless)

The wireless clients are deployed as LXD containers. LXD was chosen for the flexibility of its low-level API. We take advantage of the ability to directly assign physical host interfaces to LXC namespaces so that we can create multiple WiFi clients on a single physical host by mapping WiFi NICs to unique containers.

1. Configure the Ansible inventory 
2. Configure the `lxd_preseed.yml` file
3. Run the `deploy_lxd.yml` playbook to deploy LXD and prerequisites to the LXD hosts
4. Run `build_netplan.py`. This script queries the LXD hosts, grabbing WiFi interface names and using them to generate the `main.tf` Terraform configuration file
5. Run `terraform apply` to build the WiFi clients.
6. Run `set_wifi_test.py` to configure the WiFi containers and authenticate
7. Run `start_wifis_tgen.py` to start traffic generator processes on WiFi containers

## Deployment (Wired)

1. Configure the Ansible inventory
2. Run the `prep_tg_clients.yml` playbook
3. Configure `tg_wired_vars.yml`
4. Run `build_assets.py`
5. Terraform apply

## Launch traffic generation

1. Define traffic generation parameters (defaults to file `tg_config.yml`)
2. Run `mqtt_test.py`


# data "docker_registry_image" "{{container.tf_name}}"{
#     provider = docker.{{client.alias}}
#     name = "{{container.image}}"
# }

# resource "docker_image" "{{container.tf_name}}" {
#     provider = docker.{{client.alias}}
#     name = data.docker_registry_image.{{container.tf_name}}.name
#     pull_triggers = [data.docker_registry_image.{{container.tf_name}}.sha256_digest]
# }