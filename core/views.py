#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class WorkPageView(TemplateView):
    template_name = "work.html"


class CountdownView(TemplateView):
    template_name = "countdown.html"

    def get_context_data(self, **kwargs):
        ctx = super(CountdownView, self).get_context_data(**kwargs)

        def get_stuffs(row):
            """Aux method to generate dict for given row as input"""
            today = datetime.now()
            date = datetime.strptime(row['deadline'], "%Y/%m/%d/%H/%M/%S")
            if date < today:
                return {}

            delta = date - today
            if delta.days < 2: alert = 'danger'
            elif delta.days < 5: alert = 'warning'
            else: alert = 'success'

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
        ctx['stuffs'] = filter(lambda x: x, map(get_stuffs, rows))
        return ctx

