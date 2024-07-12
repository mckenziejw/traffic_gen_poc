from jinja2 import Environment, FileSystemLoader
import yaml
from pprint import pprint
f = open("escapes.yml")
settings = yaml.safe_load(f)
f.close()

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("test_escapes.j2")
output = template.render(settings)
print(output)