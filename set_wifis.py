from pylxd import Client
from pylxd.models.instance import Instance
#from pylxd.models.Instance import FilesManager
import argparse

# openssl req -x509 -newkey rsa:2048 -keyout lxd.key -nodes -out lxd.crt -subj "/CN=lxd.local"

client = Client(
    endpoint='https://desktop3:8443',
    verify=False
)

parser = argparse.ArgumentParser(
prog='MIST WiFi Controller',
description='Update settings on WiFi Clients'
)

parser.add_argument('-ssid')
parser.add_argument('-psk')

args = parser.parse_args()

client.authenticate('juniper123')
containers = client.instances.all()
buffer = []
for c in containers:
    f = c.FilesManager(c)
    put_file = lambda data: f.put("/etc/wpa_supplicant/wpa_supplicant.conf",data)
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_passphrase', args.ssid, args.psk], stdout_handler=put_file
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_supplicant','-B','-i','eth1','-c','/etc/wpa_supplicant/wpa_supplicant.conf']
    )
    print(exit_code,s_out,s_err)

