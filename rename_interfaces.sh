#!/bin/bash
IFACE=wl*
read macs </sys/class/net/$IFACE/address
COUNT=0
while IFS= read -r line; do
    echo "... $line ..."
done <<< "$macs"

