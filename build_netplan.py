from jinja2 import Environment, FileSystemLoader
import yaml
import psutil
import os
import re

environment = Environment(loader=FileSystemLoader("/home/lab/traffic_gen_poc/templates/"))
template = environment.get_template("netplan.j2")

wifis = {'wifis':[]}

w_list = os.listdir('/sys/class/net/')
count=1
for intf in w_list:
    if re.match('wlp[a-zA-Z0-9]*', intf):
        wifis['wifis'].append(
            {
                'name':'wlan0',
                'dev_name': intf
            }
        )
    elif re.match('wlx[a-zA-Z0-9]*', intf):
        wifis['wifis'].append(
            {
                'name':'wlan'+str(count),
                'dev_name': intf
            }
        )
        count += 1

with open('01-networkmanager-all.yaml', 'w') as out_file:
    output = template.render(w_list)
    out_file.write(output)