from jinja2 import Environment, FileSystemLoader
import yaml
import psutil
import os
import re
import paramiko
import time

def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.210.14.9', username='root', password='juniper123')

    stdin, stdout, stderr = client.exec_command('ls /sys/class/net')
    wifis_raw=[]
    for line in stdout:
        wifis_raw.append(line.strip('\n'))

    client.close()

    environment = Environment(loader=FileSystemLoader("/home/lab/traffic_gen_poc/templates/"))
    template = environment.get_template("main.tf.j2")

    count=1
    
    data = {'wifis':[]}
    for intf in wifis_raw:
        if re.match('wlp[a-zA-Z0-9]*', intf):
            data['wifis'].append(
                {
                    'name':'wlan0',
                    'dev_name': intf
                }
            )
        elif re.match('wlx[a-zA-Z0-9]*', intf):
            data['wifis'].append(
                {
                    'name':'wlan'+str(count),
                    'dev_name': intf
                }
            )
            count += 1

    with open('/home/lab/traffic_gen_poc/main.tf', 'w') as out_file:
        output = template.render(data)
        out_file.write(output)

if __name__ == "__main__":
    main()
