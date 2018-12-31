# !/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand

from core.management.services.generate_about_page_service import GenerateAboutPageService
from core.management.services.generate_cv_page_service import GenerateCVPageService
logger = logging.getLogger()


class Command(BaseCommand):
    help = u'Generates content for the About page using the file "about.md" located on this project\'s root folder.'

    def handle(self, *args, **options):
        GenerateCVPageService().call()
        GenerateAboutPageService().call()
