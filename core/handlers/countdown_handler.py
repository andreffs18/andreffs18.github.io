import os
import json
from datetime import datetime


class CountdownHandler:

    @classmethod
    def get_countdown_entries(cls, context):
        def get_stuffs(row):
            """Aux method to generate dict for given row as input"""
            today = datetime.now()
            date = datetime.strptime(row['deadline'], "%Y/%m/%d/%H/%M/%S")
            if date < today:
                return {}

            delta = date - today
            if delta.days < 2:
                alert = 'danger'
            elif delta.days < 5:
                alert = 'warning'
            else:
                alert = 'success'

            return dict([
                ('name', row['name']),
                ('deadline', row['deadline']),
                ('url', row['url']),
                ('alert', alert),
                ('date', date),
            ])

        # get all rows from my media countdown generated file
        jfile = open(os.getcwd() + "/core/media/countdown.json", "r")
        rows = json.loads(jfile.read())
        stuffs = list(filter(lambda x: x, map(get_stuffs, rows)))
        if not len(stuffs):
            stuffs.append(dict([
                ('name', "No schedule events"),
                ('deadline', datetime.now().strftime("%Y/%m/%d/%H/%M/%S")),
                ('url', "#"),
                ('alert', 'success'),
                ('date', datetime.now()),
            ]))
        context.update({'stuffs': stuffs})
        return context
