#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
import datetime

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

        todolist = [{
            'deadline': '2016/03/11/18/00/00',
            'name': ('Teste de An\xc3\xa1lise e Modela\xc3\xa7\xc3\xa3o de '
                     'Sistemas - 1\xc2\xba Teste - Alameda')
        }]

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
                'alert': alert
            })

        ctx['stuffs'] = stuffs
        return ctx

