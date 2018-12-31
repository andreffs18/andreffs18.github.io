# !/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.management.services.generate_countdown_json_service import GenerateCountdownJsonService


class Command(BaseCommand):

    help = 'Generates countdown dictionary for countdown page.'

    def handle(self, *args, **options):
        GenerateCountdownJsonService().call()
