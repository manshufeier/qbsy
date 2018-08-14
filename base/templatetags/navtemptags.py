# coding=utf-8

from django import template

register = template.Library()

import re

class MenuItem(template.Node):
    def __init__(self, paths,text):
        self.paths = paths
        self.text=text

    def render(self, context):
        is_cur=False
        path_list=self.paths.split(',')
        for path in path_list:
            if path == re.compile(r'/\d+', re.S).sub('', context['request'].path):
                is_cur=True
        return '<li class="active"><a href="%s">%s</a></li>' % (path_list[0], self.text) if is_cur else '<li class=""><a href="%s">%s</a></li>' % (path_list[0], self.text)

@register.tag
def menuitem(parser, token):
    token_list= token.split_contents()
    paths=token_list[1]
    text=token_list[2]
    return MenuItem(paths,text)