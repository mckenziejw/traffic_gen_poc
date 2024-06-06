terraform {
  required_providers {
    lxd = {
      source = "terraform-lxd/lxd"
    }
  }
}

provider "lxd" {
    generate_client_certificates = true
    accept_remote_certificate = true  

    remote {
        name = "lxd_host_1"
        scheme = "https"
        address = "10.210.14.1"
        port = "8443"
        password = "lab123"
        default = true
    }
}

resource "lxd_network" "wifi1" {
    name = "wifi1"
    remote = "lxd_host_1"
    type = "physical"
    config = {
        "parent" = "wlx9cefd5f714c6",
    }
}

resource "lxd_network" "wifi2" {
    name = "wifi2"
    remote = "lxd_host_1"
    type = "physical"
    config = {
        "parent" = "wlx9cefd5f714b8"
    }
}

resource "lxd_network" "wifi3" {
    name = "wifi3"
    remote = "lxd_host_1"
    type = "physical"
    config = {
        "parent" = "wlx9cefd5f714b5"
    }
}


resource "lxd_instance" "wifi_client_1" {
    name = "wifi-client-1"
    image = "images:kali/amd64"
    type = "container"
    remote = "lxd_host_1"
    running = true

    device  {
        name = "wifi1"
        type = "nic"
        properties = {
            "network" = "wifi1"
        }
    }

    device {
        name = "rfkill"
        type = "unix-char"
        properties = {
            "major" = 10
            "minor" = 242
            "path" = "/dev/rfkill"
            "source" = "/dev/rfkill"
        }
    }

    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }

    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]
}

resource "lxd_instance" "wifi_client_2" {
    name = "wifi-client-2"
    image = "images:kali/amd64"
    type = "container"
    remote = "lxd_host_1"
    running = true

    device  {
        name = "wifi2"
        type = "nic"
        properties = {
            "network" = "wifi2"
        }
    }
    device {
        name = "rfkill"
        type = "unix-char"
        properties = {
            "major" = 10
            "minor" = 242
            "path" = "/dev/rfkill"
            "source" = "/dev/rfkill"
        }
    }

    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }

    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]

}

resource "lxd_instance" "wifi_client_3" {
    name = "wifi-client-3"
    image = "images:kali/amd64"
    type = "container"
    remote = "lxd_host_1"
    running = true

    device  {
        name = "wifi3"
        type = "nic"
        properties = {
            "network" = "wifi3"
        }
    }
    device {
        name = "rfkill"
        type = "unix-char"
        properties = {
            "major" = 10
            "minor" = 242
            "path" = "/dev/rfkill"
            "source" = "/dev/rfkill"
        }
    }


    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }

    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]

}