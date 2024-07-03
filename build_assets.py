from jinja2 import Environment, FileSystemLoader
import yaml
from pprint import pprint
f = open("tg_wifi_vars.yml")
settings = yaml.safe_load(f)
f.close()

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("tg_wired.tf.j2")

with open('tg_wired.tf', 'w') as out_file:
    output = template.render(settings)
    out_file.write(output)