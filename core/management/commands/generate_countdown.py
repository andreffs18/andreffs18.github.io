# !/usr/bin/python
# -*- coding: utf-8 -*-
"""Created by andresilva on 8/22/16"""
import os
import json
from icalendar import Calendar
from django.core.management.base import BaseCommand

import logging
logger = logging.getLogger()

class Command(BaseCommand):
    help = ('Generates countdown dictionary for countdown page.')

    def handle(self, *args, **options):
        """"""
        # configs
        filepath = os.getcwd() + "/core/media/iCalendarSync.ics"
        if not os.path.isfile(filepath):
            raise ValueError("\"{}\" is not a file.".format(filepath))

        logger.info("Extracting events from \"{}\".".format(filepath))
        # get .ics file and extract data
        def get_fields(x):
            get_start_date = lambda x: dict(x.items()).get('DTSTART', None).dt.strftime("%Y/%m/%d/%H/%m/%S")
            get_description = lambda x: dict(x.items()).get('SUMMARY', None)
            get_url = lambda x: dict(x.items()).get('URL', None)
            return [f(x) for f in [get_start_date, get_description, get_url]]

        file = open(filepath, 'rb')
        cal = Calendar.from_ical(file.read())
        data = map(get_fields, cal.walk('vevent'))
        logger.info("Extracted {} events . Saving to \"countdown\" json file"
                    "".format(len(data)))
        countdown = [dict(
            [('deadline', deadline), ('name', description), ('url', url)]
        ) for deadline, description, url in data]

        # order by ascending date
        countdown = sorted(countdown, key=lambda x: x['deadline'])

        # save into /media folder
        filepath = os.getcwd() + "/core/media/countdown.json"

        with open(filepath, "w+") as fjson:
            fjson.write(json.dumps(countdown))
        logger.info("\"{}\" created successfully!".format(filepath))


__author__ = "andresilva"
__email__ = "andre@unbabel.com"

