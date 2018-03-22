# !/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

import logging
logger = logging.getLogger()


def minute_job():
    logger.info("Heartbeat {}".format(datetime.utcnow()))


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """"""
        sched = BlockingScheduler()

        sched.add_job(minute_job, 'interval', minutes=1)
        sched.start()

