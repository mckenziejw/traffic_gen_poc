terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

provider "docker" {
  alias    = "client1"
  host     = "ssh://lab@client1:22"
  ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
}
provider "docker" {
  alias    = "client2"
  host     = "ssh://lab@client2:22"
  ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
}
provider "docker" {
  alias    = "client3"
  host     = "ssh://lab@client3:22"
  ssh_opts = ["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"]
}

resource "docker_network" "services_net_1" {
    provider = docker.client1
    name = "services_net"
    driver = "ipvlan"

    ipam_config {
        subnet = "10.41.0.0/24"
        ip_range = "10.41.0.0/24"
        gateway = "10.41.0.1"
    }
    options = {
        parent = "eth0"
        ipvlan_mode = "l2"
    }
}
