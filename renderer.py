import codecs
import os
from jinja2 import Environment, FileSystemLoader

base_dir = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    autoescape=True,
    loader=FileSystemLoader(base_dir + "/html")
)

files = {}
for fname in os.listdir(base_dir + "/files"):
    with codecs.open(base_dir + "/files/" + fname, encoding='utf-8') as f:
        files[fname] = f.read()

def render(template_name, **kwargs):
    tmpl = env.get_template(template_name)
    return tmpl.render(files=files, **kwargs)

