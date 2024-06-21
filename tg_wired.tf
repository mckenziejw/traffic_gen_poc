terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    # remote = {
    #   source = "tenstad/remote"
    #   version = "0.1.3"
    # }
  }
}

# provider "remote" {
#     max_sessions = 3
# }

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

data "docker_registry_image" "web_client_1"{
    provider = docker.client1
    name = "autofunbot/tg_web_client:latest"
}

resource "docker_image" "web_client_1" {
    provider = docker.client1
    name = data.docker_registry_image.web_client_1.name
    pull_triggers = [data.docker_registry_image.web_client_1.sha256_digest]
}

data "docker_registry_image" "web_client_2"{
    provider = docker.client2
    name = "autofunbot/tg_web_client:latest"
}

resource "docker_image" "web_client_2" {
    provider = docker.client2
    name = data.docker_registry_image.web_client_2.name
    pull_triggers = [data.docker_registry_image.web_client_2.sha256_digest]
}
data "docker_registry_image" "web_client_3"{
    provider = docker.client3
    name = "autofunbot/tg_web_client:latest"
}

resource "docker_image" "web_client_3" {
    provider = docker.client3
    name = data.docker_registry_image.web_client_3.name
    pull_triggers = [data.docker_registry_image.web_client_3.sha256_digest]
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
    image = docker_image.web_client_1
    hostname = "web-client-1"
    host  {
        host = "web-server-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-server-3"
        ip = "10.43.0.2"
    }
    env = [
        "INTERVAL=5",
        "TARGETS=web-server-2 web-server-3",
        "MQTT_BROKER=10.41.0.7"
    ]
    depends_on = [docker_network.services_net_1, docker_container.mqtt_server_1, docker_image.web_client_1]
}
resource "docker_container" "web_client_2" {
    provider = docker.client2
    name = "web-client"
    image = docker_image.web_client_2
    hostname = "web-client-2"
    host  {
        host = "web-server-1"
        ip = "10.41.0.2"
    }
    host {
        host = "web-server-3"
        ip = "10.43.0.2"
    }
    env = [
        "INTERVAL=5",
        "TARGETS=web-server-3 web-server-1",
        "MQTT_BROKER=10.42.0.7"
    ]
    depends_on = [docker_network.services_net_2, docker_container.mqtt_server_2, docker_image.web_client_2]
}
resource "docker_container" "web_client_3" {
    provider = docker.client3
    name = "web-client"
    image = docker_image.web_client_3
    hostname = "web-client-3"
    host  {
        host = "web-server-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-server-1"
        ip = "10.41.0.2"
    }

    env = [
        "INTERVAL=5",
        "TARGETS=web-server-2 web-server-1",
        "MQTT_BROKER=10.43.0.7"
    ]
    depends_on = [docker_network.services_net_3, docker_container.mqtt_server_3, docker_image.web_client_3]
}
resource "docker_container" "web_server_1" {
    provider = docker.client1
    name = "web-server"
    image = "autofunbot/tg_web_server"
    hostname = "web-server-1"
    host  {
        host = "web-server-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-server-3"
        ip = "10.43.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.41.0.2"
    }
    env = [
        "PORT=80",
        "TARGETS=web-client-2 web-client-3"
    ]
    depends_on = [docker_network.services_net_1]
}
resource "docker_container" "web_server_2" {
    provider = docker.client2
    name = "web-server"
    image = "autofunbot/tg_web_server"
    hostname = "web-server-2"
    host  {
        host = "web-server-1"
        ip = "10.41.0.2"
    }
    host {
        host = "web-server-3"
        ip = "10.43.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.42.0.2"
    }
    env = [
        "PORT=80",
        "TARGETS=web-client-1 web-client-3"
    ]
    depends_on = [docker_network.services_net_2]
}
resource "docker_container" "web_server_3" {
    provider = docker.client3
    name = "web-server"
    image = "autofunbot/tg_web_server"
    hostname = "web-server-3"
    host  {
        host = "web-server-2"
        ip = "10.42.0.2"
    }
    host {
        host = "web-server-1"
        ip = "10.41.0.2"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.43.0.2"
    }
    env = [
        "PORT=80",
        "TARGETS=web-client-2 web-client-1"
    ]
    depends_on = [docker_network.services_net_3]
}
# create the MQTT server config

# resource "remote_file" "mqtt_conf_1" {
#     conn {
#         host = "10.41.0.254"
#         user = "lab"
#         private_key_path = "/home/lab/.ssh/id_rsa"
#     }
#     path = "/home/lab/mosquitto.conf"
#     content = templatefile("templates/mosquitto.conf.tftpl",{})
#     permissions = "0644"
# }
# resource "remote_file" "mqtt_conf_2" {
#     conn {
#         host = "10.42.0.254"
#         user = "lab"
#         password = "lab123"
#     }
#     path = "/home/lab/mosquitto.conf"
#     content = templatefile("templates/mosquitto.conf.tftpl",{})
#     permissions = "0644"
# }

# resource "remote_file" "mqtt_conf_3" {
#     conn {
#         host = "10.43.0.254"
#         user = "lab"
#         password = "lab123"
#     }
#     path = "/home/lab/mosquitto.conf"
#     content = templatefile("templates/mosquitto.conf.tftpl",{})
#     permissions = "0644"
# }

resource "docker_container" "mqtt_server_1"{
    provider = docker.client1
    name = "mqtt_server"
    image = "eclipse-mosquitto"

    mounts {
        target = "/mosquitto/config/mosquitto.conf"
        source = "/home/lab/mosquitto/mosquitto.conf"
        type = "bind"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.41.0.7"
    }
}

resource "docker_container" "mqtt_server_2"{
    provider = docker.client2
    name = "mqtt_server"
    image = "eclipse-mosquitto"

    mounts {
        target = "/mosquitto/config/mosquitto.conf"
        source = "/home/lab/mosquitto/mosquitto.conf"
        type = "bind"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.42.0.7"
    }
}

resource "docker_container" "mqtt_server_3"{
    provider = docker.client3
    name = "mqtt_server"
    image = "eclipse-mosquitto"

    mounts {
        target = "/mosquitto/config/mosquitto.conf"
        source = "/home/lab/mosquitto/mosquitto.conf"
        type = "bind"
    }

    networks_advanced {
        name = "services_net"
        ipv4_address = "10.43.0.7"
    }
}