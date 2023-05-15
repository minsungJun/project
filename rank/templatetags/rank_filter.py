from django import template
register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    return value - arg

@register.filter(name='win_rate')
def win_rate(value, arg):
    return round(float(value)/float(arg)*100, 3)