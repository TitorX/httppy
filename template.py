# coding=utf-8
import jinja2
import os


def get_template_render(path):

    class _Render:

        path = ''

        def __init__(self):
            self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.path))

        def render(self, template, *args, **kwargs):
            content = self.env.get_template(template).render(*args, **kwargs)
            if type(content) is unicode:
                content = content.encode('utf-8')
            return content

    setattr(_Render, 'path', os.path.abspath(path))
    return _Render()

Render = get_template_render('template')


def render(template, *args, **kwargs):
    return Render.render(template, *args, **kwargs)
