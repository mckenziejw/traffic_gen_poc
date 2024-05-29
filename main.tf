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
        address = "10.210.40.164"
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
        "parent" = "ens192",
    }
}

resource "lxd_network" "wifi2" {
    name = "wifi2"
    remote = "lxd_host_1"
    type = "physical"
    config = {
        "parent" = "ens224"
    }
}

resource "lxd_network" "wifi3" {
    name = "wifi3"
    remote = "lxd_host_1"
    type = "physical"
    config = {
        "parent" = "ens256"
    }
}


resource "lxd_instance" "wifi_client_1" {
    name = "wifi-client-1"
    image = "alpine/3.20"
    type = "container"
    remote = "lxd_host_1"
    running = false

    device  {
        name = "wifi1"
        type = "nic"
        properties = {
            "network" = "wifi1"
        }
    }

    config = {
        "boot.autostart" = true
    }

    execs = {
        "set_path" = {
            command = ["/bin/ash", "export PATH=/bin:/usr/bin:/sbin"]
        }
        "add_depends" = {
            command = ["/bin/ash", "apk add --no-cache python3 findmnt curl libcap bind-tools wireless-tools wpa_supplicant"]
        }
        "configure_supplicant" = {
            command = ["/bin/ash", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
        }
        "Enable WPA supplicant" = {
            command = ["/bin/ash", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
        }
    }

    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]
}

resource "lxd_instance" "wifi_client_2" {
    name = "wifi-client-2"
    image = "alpine/3.20"
    type = "container"
    remote = "lxd_host_1"
    running = false

    device  {
        name = "wifi2"
        type = "nic"
        properties = {
            "network" = "wifi2"
        }
    }

    config = {
        "boot.autostart" = true
    }
    execs = {
        "set_path" = {
            command = ["/bin/ash", "export PATH=/bin:/usr/bin:/sbin"]
        }
        "add_depends" = {
            command = ["/bin/ash", "apk add --no-cache python3 findmnt curl libcap bind-tools wireless-tools wpa_supplicant"]
        }
        "configure_supplicant" = {
            command = ["/bin/ash", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
        }
        "Enable WPA supplicant" = {
            command = ["/bin/ash", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
        }
    }
    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]

}

resource "lxd_instance" "wifi_client_3" {
    name = "wifi-client-3"
    image = "alpine/3.20"
    type = "container"
    remote = "lxd_host_1"
    running = false

    device  {
        name = "wifi3"
        type = "nic"
        properties = {
            "network" = "wifi3"
        }
    }

    config = {
        "boot.autostart" = true
    }
    execs = {
        "set_path" = {
            command = ["/bin/ash", "export PATH=/bin:/usr/bin:/sbin"]
        }
        "add_depends" = {
            command = ["/bin/ash", "apk add --no-cache python3 findmnt curl libcap bind-tools wireless-tools wpa_supplicant"]
        }
        "configure_supplicant" = {
            command = ["/bin/ash", "wpa_passphrase '$wifi_ssid' '$wifi_psk' > /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wifi_psk" = "psk_goes_here"
                "wifi_ssid" = "ssid_goes_here"
            }
        }
        "Enable WPA supplicant" = {
            command = ["/bin/ash", "wpa_supplicant -B -i $wlan -c /etc/wpa_supplicant/wpa_supplicant.conf"]
            environment = {
                "wlan" = "wlan0"
            }
        }
    }
    depends_on = [lxd_network.wifi1, lxd_network.wifi2, lxd_network.wifi3]

}