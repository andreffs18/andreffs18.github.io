# !/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from core.management.scripts.chat_test import run_test

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
        sched.add_job(run_test, 'cron', hour=8, minute=0)
        sched.start()

