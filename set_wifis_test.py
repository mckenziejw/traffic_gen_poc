## For testing the reboot, run `nmcli connection modify <connection> connection.autoconnect yes` on client-1

from pylxd import Client
from pylxd.models.instance import Instance
from pprint import pprint
import time
import argparse

import warnings
warnings.filterwarnings('ignore')
# openssl req -x509 -newkey rsa:2048 -keyout lxd.key -nodes -out lxd.crt -subj "/CN=lxd.local"

parser = argparse.ArgumentParser()
parser.add_argument('-wifi_host', default='lxdhost')
parser.add_argument('-ssid', default='WLAN_TEST')
parser.add_argument('-psk', default='juniper123')
parser.add_argument('-wifi_host_password', default='juniper123')
args = parser.parse_args()
client = Client(
    endpoint=f"https://{args.wifi_host}:8443",
    verify=False
)
gateway = '10.99.99.1'

client.authenticate(args.wifi_host_password)

psk = args.psk
ssid = args.ssid

def create_wpa_conf(data):
    data = f"{data}\nmac_addr=0\npreassoc_mac_addr=0\ngas_rand_mac_addr=0"
    return data
for i in range(1,5):
    c = client.instances.get('wifi-client-{}'.format(i))
    f = c.FilesManager(c)
    put_file = lambda data: f.put("/etc/wpa_supplicant/wpa_supplicant.conf",create_wpa_conf(data))
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_passphrase', ssid, psk], stdout_handler=put_file
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_supplicant','-B','-i','eth1','-c','/etc/wpa_supplicant/wpa_supplicant.conf']
    )
    if(exit_code == 0):
        print('wifi-client-{} WPA supplicant successfully configured'.format(i))
    else:
        print('wifi-client-{} WPA supplicant failed'.format(i))
        print(exit_code,s_out,s_err)
    time.sleep(10)
    #pprint(c.state().network['eth1'])
    ip_assigned = False
    for a in c.state().network['eth1']['addresses']:
        if a['family'] == 'inet' and a['address'] != '':
            ip_assigned = True
            print('wifi-client-{} WPA IP Assigned'.format(i))
    if not ip_assigned:
        print('wifi-client-{} WPA DHCP did not start, running manually...'.format(i))
        exit_code,s_out,s_err = c.execute(
        commands = ['dhclient','eth1']
        )
        if(exit_code == 0):
            print('wifi-client-{} WPA DHCP manual configuration worked'.format(i))
        else:
            print('wifi-client-{} WPA DHCP manual configuration failed'.format(i))
    time.sleep(10)
    print("Updating route table")
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','delete','default']
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','add','default', 'via', gateway]
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','add','192.168.0.0/16', 'via', '192.168.10.1']
    )
    print("Running ping test for wifi-client-{}".format(i))
    exit_code,s_out,s_err = c.execute(
        commands = ['ping','-c', '4','8.8.8.8']
        )
    print(exit_code,s_out,s_err)