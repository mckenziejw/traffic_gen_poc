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