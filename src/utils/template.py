from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(["templates"]))


def generate_template(template_name: str, data: dict):
    template = env.get_template(template_name)
    return template.render(data)
