from jinja2 import Environment, FileSystemLoader
import yaml
import psutil
import os
import re
import paramiko
import time
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="WiFi Traffic Generator Terraform Templating Tool",
        description="This script crates the terraform module to deploy LXD WiFi Clients"
    )

    parser.add_argument('-lxd_host')
    parser.add_argument('-user', default='lab')
    parser.add_argument('-host_password', default='juniper123')
    parser.add_argument('-lxd_password', default='juniper123')
    args = parser.parse_args()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(args.lxd_host, username=args.user, password=args.host_password)

    stdin, stdout, stderr = client.exec_command('ls /sys/class/net')
    wifis_raw=[]
    for line in stdout:
        wifis_raw.append(line.strip('\n'))

    client.close()
    print(wifis_raw)
    environment = Environment(loader=FileSystemLoader("./templates/"))
    template = environment.get_template("main.tf.j2")

    count=1
    
    data = {
        'wifis':[],
        'lxd_host': args.lxd_host,
        'lxd_password': args.lxd_password
    }
    for intf in wifis_raw:
        print(f"checking {intf}")
        if re.match('wlp[a-zA-Z0-9]*', intf):
            print(f"match found for {intf}")
            data['wifis'].append(
                {
                    'name':'wlan0',
                    'dev_name': intf
                }
            )
        elif re.match('wlx[a-zA-Z0-9]*', intf):
            print(f"match found for {intf}")
            data['wifis'].append(
                {
                    'name':'wlan'+str(count),
                    'dev_name': intf
                }
            )
            count += 1
    print(data)
    with open('main.tf', 'w') as out_file:
        output = template.render(data)
        out_file.write(output)

if __name__ == "__main__":
    main()
