from jinja2 import Environment, FileSystemLoader
import yaml

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("compose.j2")

f = open("settings.yml")
settings = yaml.safe_load(f)
f.close()

with open('compose.yml', 'w') as out_file:
    output = template.render(settings)
    out_file.write(output)