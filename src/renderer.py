
from jinja2 import Environment, BaseLoader, StrictUndefined
import markdown

env = Environment(
    loader=BaseLoader(),
    autoescape=True,
    undefined=StrictUndefined
)

def render_email(subject_tmpl, body_md_tmpl, context):
    subject = env.from_string(subject_tmpl).render(**context)
    body_md = env.from_string(body_md_tmpl).render(**context)
    html = markdown.markdown(body_md, extensions=["extra"])
    return subject, html
