from django import template
register = template.Library()

@register.filter(is_safe=False)
def gen_page_url(value,arg):
    import re
    curpath = value.get_full_path()
    dr = re.compile(r'page=[0-9]*', re.S)
    dd = dr.sub('', curpath)
    if '?' not in dd:
        dd = dd + '?'
    if not dd.endswith('&') and not dd.endswith('?'):
        dd = dd + '&'
    dd = dd + 'page=%s' % arg
    return dd

@register.filter(is_safe=False)
def get_query_count(value):
    return len(value)