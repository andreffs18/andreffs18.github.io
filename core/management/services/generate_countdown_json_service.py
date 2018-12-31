import os
import json
import logging
from tqdm import tqdm
from icalendar import Calendar

logger = logging.getLogger(__name__)


class GenerateCountdownJsonService:

    def __init__(self, filepath=os.getcwd() + "/core/media/calendars/"):
        self.filepath = filepath
        self.target_countdown_filepath = os.getcwd() + "/core/media/countdown.json"

    def _get_all_calendars(self):
        calendars = []
        for f in os.listdir(self.filepath):
            if os.path.isfile(os.path.join(self.filepath, f)):
                calendars.append(os.path.join(self.filepath, f))
        return calendars

    def _get_fields(self, args):
        # get .ics file and extract data
        get_start_date = lambda x: dict(x.items()).get('DTSTART', None).dt.strftime("%Y/%m/%d/%H/%m/%S")
        get_description = lambda x: dict(x.items()).get('SUMMARY', None)
        get_url = lambda x: dict(x.items()).get('URL', None)
        return [f(args) for f in [get_start_date, get_description, get_url]]

    def call(self):
        calendars = self._get_all_calendars()
        logger.info(u"Extracting events from {} calendars.".format(len(calendars)))

        countdown = []
        for calendar in tqdm(calendars):
            with open(calendar, 'rb') as calendar:
                calendar = Calendar.from_ical(calendar.read())
                data = list(map(self._get_fields, calendar.walk('vevent')))
                countdown.extend([{'deadline': deadline, 'name': description, 'url': url}
                                  for deadline, description, url in data])

        # order by ascending date
        countdown = sorted(countdown, key=lambda x: x['deadline'])

        # save into /media folder
        with open(self.target_countdown_filepath, "w+") as target_file:
            target_file.write(json.dumps(countdown))
        logger.info(u'"{}" created successfully!'.format(self.target_countdown_filepath))
