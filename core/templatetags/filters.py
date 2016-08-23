from django import template
register = template.Library()

import logging
logger = logging.getLogger(__name__)

@register.filter
def to_upper(string):
    return string.upper()


@register.filter
def to_lower(string):
    return string.lower()


@register.filter
def get_item(item, string):
    try:
        return item[string]
    except:
        logger.exception("Failed to get value {} {}".format(item, string))
        logger.error(item)
        return ""