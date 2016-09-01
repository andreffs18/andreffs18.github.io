#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import datetime
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
        jfile = open(os.getcwd() + "/core/media/countdown.json", "r")
        todolist = json.loads(jfile.read())

        stuffs = []
        now = datetime.datetime.now()
        for stuff in todolist:
            date = datetime.datetime.strptime(
                stuff['deadline'], "%Y/%m/%d/%H/%M/%S")
            if date < now:
                continue

            delta = date - now

            if delta.days < 2:
                alert = 'danger'
            elif delta.days < 5:
                alert = 'warning'
            else:
                alert = 'success'

            stuffs.append({
                'name': stuff['name'],
                'deadline': stuff['deadline'],
                'alert': alert,
                'url': stuff['url'],
            })

        ctx['stuffs'] = stuffs
        return ctx

