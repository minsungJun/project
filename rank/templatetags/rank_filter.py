from django import template
register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    return value - arg

@register.filter(name='win_rate')
def win_rate(value, arg):
    if arg == 0:
        return value
    return round(float(value)/float(arg)*100, 3)

@register.filter(name='mul')
def mul(value, arg):
    return value * arg