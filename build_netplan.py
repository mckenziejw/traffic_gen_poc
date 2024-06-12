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
    client.connect('10.210.14.1', username='lab', password='lab123')

    stdin, stdout, stderr = client.exec_command('ls /sys/class/net')
    wifis=[]
    for line in stdout:
        wifis.append(line.strip('\n'))
    print(wifis)
    client.close()

if __name__ == "__main__":
    main()
# environment = Environment(loader=FileSystemLoader("/home/lab/traffic_gen_poc/templates/"))
# template = environment.get_template("main.tf.j2")

# wifis = {'wifis':[]}

# w_list = os.listdir('/sys/class/net/')
# count=1
# for intf in w_list:
#     if re.match('wlp[a-zA-Z0-9]*', intf):
#         wifis['wifis'].append(
#             {
#                 'name':'wlan0',
#                 'dev_name': intf
#             }
#         )
#     elif re.match('wlx[a-zA-Z0-9]*', intf):
#         wifis['wifis'].append(
#             {
#                 'name':'wlan'+str(count),
#                 'dev_name': intf
#             }
#         )
#         count += 1

# with open('/home/lab/traffic_gen_poc/main.tf', 'w') as out_file:
#     output = template.render(wifis)
#     out_file.write(output)