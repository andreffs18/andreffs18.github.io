#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView, View
import andreffs.utils as affsutils
import datetime
import json

class HomepageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomepageView, self).get_context_data(**kwargs)
        return ctx


class CountdownView(TemplateView):
    template_name = "countdown.html"

    def get_context_data(self, **kwargs):
        ctx = super(CountdownView, self).get_context_data(**kwargs)
        todolist = [
            {
                'name': 'Projecto CG 4º Entrega',
                'deadline': datetime.datetime(2015, 11, 23, 12, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Projecto IA 2º Entrega',
                'deadline': datetime.datetime(2015, 11, 30, 12, 30).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Projecto IA 3º Entrega',
                'deadline': datetime.datetime(2015, 12, 9, 12, 30).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': '2º Teste de ACED',
                'deadline': datetime.datetime(2015, 12, 19, 11, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': '2º Teste de PE',
                'deadline': datetime.datetime(2016, 1, 7, 9, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de Redes',
                'deadline': datetime.datetime(2016, 1, 9, 11, 30).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de CG (Repescagem 2º Teste)',
                'deadline': datetime.datetime(2016, 1, 12, 15, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': '2º Teste de IA',
                'deadline': datetime.datetime(2016, 1, 14, 18, 30).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de ACED',
                'deadline': datetime.datetime(2016, 1, 25, 15, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de PE (Repescagem)',
                'deadline': datetime.datetime(2016, 1, 26, 15, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de Redes (Repescagem)',
                'deadline': datetime.datetime(2016, 1, 27, 8, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            },
            {
                'name': 'Exame de IA (Repescagem)',
                'deadline': datetime.datetime(2016, 1, 29, 18, 00).strftime(
                    "%Y/%m/%d/%H/%M/%S"),
            }
        ]

        stuffs = []
        now = datetime.datetime.now()
        for stuff in todolist:
            date = datetime.datetime.strptime(stuff['deadline'],
                                              "%Y/%m/%d/%H/%M/%S")
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

class TimelineView(TemplateView):
    template_name = "timeline.html"

    def get_context_data(self, **kwargs):
        ctx = super(TimelineView, self).get_context_data(**kwargs)
        return ctx


class AboutpageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        ctx = super(AboutpageView, self).get_context_data(**kwargs)
        return ctx


class WorkpageView(TemplateView):
    template_name = "work.html"

    def get_context_data(self, **kwargs):
        ctx = super(WorkpageView, self).get_context_data(**kwargs)
        return ctx