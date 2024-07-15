from jinja2 import Environment, FileSystemLoader
import yaml
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-env_file', default='tg_wired_vars.yml')
parser.add_argument('-out_file', default='tg_wired.tf')
args = parser.parse_args()


f = open(args.env_file)
settings = yaml.safe_load(f)
f.close()

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("tg_wired.tf.j2")

with open('tg_wired.tf', 'w') as out_file:
    output = template.render(settings)
    out_file.write(output)