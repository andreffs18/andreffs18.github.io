from django import template
from core.settings import logger
import datetime

register = template.Library()


@register.filter(name='timestamp')
def timestamp(ts):
    if not ts:
       return 'ups'
    if ts == '':
        return 'Not defined'
    return datetime.datetime.fromtimestamp(float(ts)).strftime('%d %B %Y, %Hh%M')