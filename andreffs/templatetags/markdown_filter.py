""" Created by andresilva on 12/23/15"""
__author__ = 'andresilva'
__version__ = "1.0.0"
__email__ = "andre@unbabel.com"

from django import template
import markdown

register = template.Library()

@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text)