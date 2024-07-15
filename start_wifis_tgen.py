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
parser.add_argument('-wifi_host_password', default='juniper123')
parser.add_argument('-mqtt_server', default='192.168.10.117')
parser.add_argument('-tgtype',default='web')
parser.add_argument('-port', default=1883)
parser.add_argument('-ss_count', default=10)
parser.add_argument('-refresh_repo', default=0, type=int)
args = parser.parse_args()
client = Client(
    endpoint=f"https://{args.wifi_host}:8443",
    verify=False
)

client.authenticate(args.wifi_host_password)
wifis = [
    {'name':'wifi-client-1', 'role':'IoT'},
    {'name':'wifi-client-2', 'role':'IoT'},
    {'name':'wifi-client-3', 'role':'IoT'},
    {'name':'wifi-client-4', 'role':'Guest'}
]
for i in wifis:
    c = client.instances.get(i['name'])
    f = c.FilesManager(c)
    if(args.refresh_repo == 1):
        exit_code,s_out,s_err = c.execute(
            commands = ['git','clone','https://github.com/mckenziejw/traffic_gen_poc']
        )
    exit_code,s_out,s_err = c.execute(
        commands = ['chmod','+x','traffic_gen_poc/web_client/app.py']
    )
    exit_code, s_out, s_err = c.execute(
        commands = ['nohup', '/root/traffic_gen_poc/app.py', '-mqtt_server', args.mqtt_server, '-hostname',
                    i['name'], '-tgtype', args.tgtype, '-ss_count', args.ss_count, '-port', int(args.port), '&']
    )