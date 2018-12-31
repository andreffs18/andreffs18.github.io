# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from django.core.management.base import BaseCommand

from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger()


def minute_job():
    logger.info("Heartbeat {}".format(datetime.utcnow()))


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        """"""
        scheduler = BlockingScheduler()

        scheduler.add_job(minute_job, 'interval', minutes=1)
        scheduler.start()

