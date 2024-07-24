from jinja2 import Environment, FileSystemLoader
import yaml
from pprint import pprint
import argparse



environment = Environment(loader=FileSystemLoader("."))
template = environment.get_template("docker-compose.yml.j2")

settings = {'hosts':[]}

with open('hosts', 'r') as f:
    for l in f.readlines():
        h = l.split("    ")
        settings['hosts'].append({
            'ip': h[0].strip(),
            'name': h[1].strip()
        })

with open('docker-compose.yml', 'w') as out_file:
    output = template.render(settings)
    out_file.write(output)
    