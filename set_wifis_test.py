from pylxd import Client
from pylxd.models.instance import Instance
from pprint import pprint
import time

import argparse

# openssl req -x509 -newkey rsa:2048 -keyout lxd.key -nodes -out lxd.crt -subj "/CN=lxd.local"

client = Client(
    endpoint='https://wifi-host:8443',
    verify=False
)

# parser = argparse.ArgumentParser(
# prog='MIST WiFi Controller',
# description='Update settings on WiFi Clients with self-test AP'
# )

# parser.add_argument('-ssid')
# parser.add_argument('-psk')

# args = parser.parse_args()

client.authenticate('lab123')
## Provision the AP
ap = client.instances.get('wifi-client-1')
ssid = ap.state().network['eth1']['hwaddr'].replace(':','')
psk = 'lab123lab123'
print("Installing AP dependencies")
exit_code,s_out,s_err = ap.execute(
    commands = ['apt','install','-y','network-manager']
)
print(exit_code,s_out,s_err)
print("Configuring AP hotspot with name {}".format(ssid))
exit_code,s_out,s_err = ap.execute(
    commands = ['nmcli','device','wifi','hotspot','ifname','eth1','con-name',ssid, 'ssid', ssid, 'password', psk]
)
print(exit_code,s_out,s_err)
if(exit_code == 0):
    print("AP Successfully enabled")
else:
    print("AP initialization failed")
time.sleep(10)
for i in range(2,5):
    c = client.instances.get('wifi-client-{}'.format(i))
    f = c.FilesManager(c)
    put_file = lambda data: f.put("/etc/wpa_supplicant/wpa_supplicant.conf",data)
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_passphrase', ssid, psk], stdout_handler=put_file
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_supplicant','-B','-i','eth1','-c','/etc/wpa_supplicant/wpa_supplicant.conf']
    )
    print(exit_code,s_out,s_err)
    time.sleep(20)
    if(c.state(),network['eth1']['address'] == ''):
        exit_code,s_out,s_err = c.execute(
        commands = ['dhclient','eth1']
        )
        print(exit_code,s_out,s_err)

