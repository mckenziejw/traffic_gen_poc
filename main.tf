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

    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }

    execs = {

        "a" = {
            command = ["/bin/bash", "-c", "apt update"]
            trigger = "once"
        }
        "b" = {
            command = ["/bin/bash", "-c", "apt install -y wpasupplicant python3 curl wireless-tools git kali-tools-wireless"]
            trigger = "once"
        }
        "c" = {
            command = ["/bin/bash", "-c", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
            trigger = "once"
        }
        "d" = {
            command = ["/bin/bash", "-c", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
            trigger = "once"
        }
        "e" = {
            command = ["/bin/bash", "-c", "git clone https://github.com/mckenziejw/traffic_gen_poc"]
            trigger = "once"
        }
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

    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }
    execs = {

        "a" = {
            command = ["/bin/bash", "-c", "apt update"]
            trigger = "once"
        }
        "b" = {
            command = ["/bin/bash", "-c", "apt install -y wpasupplicant python3 curl wireless-tools git kali-tools-wireless"]
            trigger = "once"
        }
        "c" = {
            command = ["/bin/bash", "-c", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
            trigger = "once"
        }
        "d" = {
            command = ["/bin/bash", "-c", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
            trigger = "once"
        }
        "e" = {
            command = ["/bin/bash", "-c", "git clone https://github.com/mckenziejw/traffic_gen_poc"]
            trigger = "once"
        }
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

    config = {
        "boot.autostart" = true
        "security.privileged" = true
    }
    execs = {

        "a" = {
            command = ["/bin/bash", "-c", "apt update"]
            trigger = "once"
        }
        "b" = {
            command = ["/bin/bash", "-c", "apt install -y wpasupplicant python3 curl wireless-tools git kali-tools-wireless"]
            trigger = "once"
        }
        "c" = {
            command = ["/bin/bash", "-c", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
            trigger = "once"
        }
        "d" = {
            command = ["/bin/bash", "-c", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
            trigger = "once"
        }
        "e" = {
            command = ["/bin/bash", "-c", "git clone https://github.com/mckenziejw/traffic_gen_poc"]
            trigger = "once"
        }
    }
    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]

}