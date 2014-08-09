from django.template.defaultfilters import slugify
from core.settings import AVG_WORDS_PER_MINUTE
import datetime

'''
    Creates a url readable link
'''
def generate_slug(string, timestamp):
    time = datetime.datetime.fromtimestamp(timestamp)
    return "%s/%s/%s/%s" % (time.day, time.month, time.year, slugify(string))

'''
    Calculates the average time that an article takes to read
'''
def calc_avg_read_time(text):
    total_chars = count_chars(text)
    read_time_in_seconds = (float(total_chars) / AVG_WORDS_PER_MINUTE) * 60

    ## convert time into the specific format
    time = datetime.datetime.fromtimestamp(read_time_in_seconds)
    time = time.strftime("%Mm%Ss")

    ## just erase the first number if it is a zero
    if time[0] == "0":
        time = time[1:]


    return time

'''
    Counts the number of letters of a string
'''
def count_chars(word):
    return len(word) - word.count(' ')