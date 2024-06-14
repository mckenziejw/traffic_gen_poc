#!/bin/sh -e
/usr/sbin/wpa_supplicant -B -i eth1 -c /etc/wpa_supplicant/wpa_supplicant.conf
/usr/sbin/dhclient eth1