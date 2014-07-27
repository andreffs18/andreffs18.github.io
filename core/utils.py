from django.template.defaultfilters import slugify
import datetime
'''
    Creates a url readable link
'''
def generate_slug(string, timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return "%s/%s/%s/%s" % (time.day, time.month, time.year, slugify(string))