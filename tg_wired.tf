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
resource "docker_network" "services_net_2" {
    provider = docker.client2
    name = "services_net"
    driver = "ipvlan"

    ipam_config {
        subnet = "10.42.0.0/24"
        ip_range = "10.42.0.0/24"
        gateway = "10.42.0.1"
    }
    options = {
        parent = "eth0"
        ipvlan_mode = "l2"
    }
}
resource "docker_network" "services_net_3" {
    provider = docker.client3
    name = "services_net"
    driver = "ipvlan"

    ipam_config {
        subnet = "10.43.0.0/24"
        ip_range = "10.43.0.0/24"
        gateway = "10.43.0.1"
    }
    options = {
        parent = "eth0"
        ipvlan_mode = "l2"
    }
}

resource "docker_container" "web_client_1" {
    provider = docker.client1
    name = "web-client"
    image = "autofunbot/tg_web_client"
    hostname = "web-client-1"
    host  {
        host = "web-client-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-client-3"
        ip = "10.43.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.41.0.2"
    }
    env = [
        "INTERVAL=5",
        "TARGETS=web-client-2 web-client-3"
    ]
}
resource "docker_container" "web_client_2" {
    provider = docker.client2
    name = "web-client"
    image = "autofunbot/tg_web_client"
    hostname = "web-client-2"
    host  {
        host = "web-client-1"
        ip = "10.41.0.2"
    }
    host {
        host = "web-client-3"
        ip = "10.43.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.42.0.2"
    }
    env = [
        "INTERVAL=5",
        "TARGETS=web-client-3 web-client-1"
    ]
}
resource "docker_container" "web_client_3" {
    provider = docker.client3
    name = "web-client"
    image = "autofunbot/tg_web_client"
    hostname = "web-client-3"
    host  {
        host = "web-client-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-client-1"
        ip = "10.41.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.43.0.2"
    }
    env = [
        "INTERVAL=5",
        "TARGETS=web-client-2 web-client-1"
    ]
}
