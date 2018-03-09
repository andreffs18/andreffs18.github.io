# !/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from core.management.scripts.chat_test import run_test

import logging
logger = logging.getLogger()


def timed_job():
    print('This job is run every three minutes.')


def scheduled_job():
    print('This job is run every weekday at 5pm.')


def minute_job():
    logger.info("MODAFOQUING {} CLICk".format(datetime.utcnow()))


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """"""
        sched = BlockingScheduler()

        sched.add_job(minute_job, 'interval', minutes=1)
        # sched.add_job(timed_job, 'interval', minutes=3)
        # sched.add_job(scheduled_job, 'cron', day_of_week='mon-fri', hour=17)
        sched.add_job(run_test, 'cron', hour=19, minutes=30)
        sched.start()

