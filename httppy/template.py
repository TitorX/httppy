__author__ = 'titorx'

import jinja2
import os


def get_template_render(path):

    class Render:

        path = ''

        def __init__(self):
            self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.path))

        def render(self, template, *args, **kwargs):
            return self.env.get_template(template).render(args=args, kwargs=kwargs)

    setattr(Render, 'path', os.path.abspath(path))
    return Render()

render = get_template_render('template')
