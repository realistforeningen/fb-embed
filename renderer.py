import codecs
import os
from jinja2 import Environment, FileSystemLoader

base_dir = os.path.dirname(os.path.abspath(__file__))

env = Environment(
    autoescape=True,
    loader=FileSystemLoader(base_dir + "/html")
)

styles = {}
for fname in os.listdir(base_dir + "/css"):
    name = os.path.splitext(fname)[0]
    with codecs.open(base_dir + "/css/" + fname, encoding='utf-8') as f:
        styles[name] = f.read()

def render(template_name, **kwargs):
    tmpl = env.get_template(template_name)
    return tmpl.render(styles=styles, **kwargs)

