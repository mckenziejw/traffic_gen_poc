## For testing the reboot, run `nmcli connection modify <connection> connection.autoconnect yes` on client-1

from pylxd import Client
from pylxd.models.instance import Instance
from pprint import pprint
import time
import argparse
import requests
import mistapi
from mistapi.api import v1 as mist
import warnings
warnings.filterwarnings('ignore')
# openssl req -x509 -newkey rsa:2048 -keyout lxd.key -nodes -out lxd.crt -subj "/CN=lxd.local"

parser = argparse.ArgumentParser()
parser.add_argument('-wifi_host', default='lxdhost')
parser.add_argument('-wifi_host_password', default='juniper123')
parser.add_argument('-api_token')
parser.add_argument('-org_id')
parser.add_argument('-ssid')
parser.add_argument('-ssid_guest')
args = parser.parse_args()
client = Client(
    endpoint=f"https://{args.wifi_host}:8443",
    verify=False
)
gateway = '10.99.99.1'

client.authenticate(args.wifi_host_password)

ssid = args.ssid
guest_ssid = args.ssid_guest
org_id = args.org_id
api_token = args.api_token
wifis = [
    {'name':'wifi-client-1', 'role':'IoT'},
    {'name':'wifi-client-2', 'role':'IoT'},
    {'name':'wifi-client-3', 'role':'IoT'},
    {'name':'wifi-client-4', 'role':'Guest'}
]

def create_wpa_conf(data):
    data = f"{data}\nmac_addr=0\npreassoc_mac_addr=0\ngas_rand_mac_addr=0\np2p_disabled=1"
    return data

def get_latest_psk(client):
    mist_api_root = "https://api.mist.com/api/v1/"
    auth_uri = f"orgs/{org_id}/apitokens"
    session = mistapi.APISession(apitoken=api_token, host='api.mist.com')
    session.login()
    psks = mist.orgs.psks.listOrgPsks(session, org_id=org_id).data
    psk_id = None
    last_date = 0
    last_expiry = None
    # Check for psks without expiry
    for p in psks:
        if p['role'] == client['role']:
            ## If the psk does not expire, prefer that one and only check for other psks without expiry
            if p['expire_time'] is None:
                if psk_id is None:
                    last_date = p['modified_time']
                    psk_id = p['id']
                elif last_date < p['modified_time']:
                    last_date = p['modified_time']
                    psk_id = p['id']
    if psk_id is not None:
        print("permanent psk found")
        psk = mist.orgs.psks.getOrgPsk(session, org_id=org_id, psk_id=psk_id).data['passphrase']
        return psk
    # Is a permanent psk was not found, find the one with the latest expiration date
    for p in psks:
        if p['role'] == client['role']:
            if last_expiry is None:
                if last_expiry is None:
                    last_expiry = p['expire_time']
                    psk_id = p['id']
                elif last_expiry < p['expire_time']:
                    last_expiry = p['expire_time']
                    psk_id = p['id']
    if psk_id is None:
        return None
    else:
        psk = psk = mist.orgs.psks.getOrgPsk(session, org_id=org_id, psk_id=psk_id).data['passphrase']
        return psk

for wifi in wifis:
    c = client.instances.get(wifi['name'])
    f = c.FilesManager(c)
    psk = get_latest_psk(wifi)
    put_file = lambda data: f.put("/etc/wpa_supplicant/wpa_supplicant.conf",data)
    if wifi['role'] == 'Guest':
        exit_code,s_out,s_err = c.execute(
            commands = ['wpa_passphrase', guest_ssid, psk], stdout_handler=put_file
        )
    else:
        exit_code,s_out,s_err = c.execute(
            commands = ['wpa_passphrase', ssid, psk], stdout_handler=put_file
        )
    exit_code,s_out,s_err = c.execute(
        commands = ['killall','wpa_supplicant']
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['wpa_supplicant','-B','-i','eth1','-c','/etc/wpa_supplicant/wpa_supplicant.conf']
    )
    if(exit_code == 0):
        print(f"{wifi['name']} WPA supplicant successfully configured")
    else:
        print(f"{wifi['name']} WPA supplicant failed")
        print(exit_code,s_out,s_err)
    time.sleep(10)
    #pprint(c.state().network['eth1'])
    ip_assigned = False
    for a in c.state().network['eth1']['addresses']:
        if a['family'] == 'inet' and a['address'] != '':
            ip_assigned = True
            print(f"{wifi['name']} WPA IP Assigned")
    if not ip_assigned:
        print(f"{wifi['name']} WPA DHCP did not start, running manually...")
        exit_code,s_out,s_err = c.execute(
        commands = ['dhclient','eth1']
        )
        if(exit_code == 0):
            print(f"{wifi['name']}WPA DHCP manual configuration worked")
        else:
            print(f"{wifi['name']} WPA DHCP manual configuration failed")
    time.sleep(10)
    print("Updating route table")
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','delete','default']
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','add','default', 'via', gateway]
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'link','set','eth0', 'up']
    )
    exit_code,s_out,s_err = c.execute(
        commands = ['ip', 'route','add','192.168.0.0/16', 'via', '10.120.0.1']
    )
    print(f"Running ping test for {wifi['name']}")
    exit_code,s_out,s_err = c.execute(
        commands = ['ping','-c', '4','8.8.8.8']
        )
    print(exit_code,s_out,s_err)
    exit_code,s_out,s_err = c.execute(
        commands = ['ping','-c', '4','192.168.10.1']
        )
    print(exit_code,s_out,s_err)