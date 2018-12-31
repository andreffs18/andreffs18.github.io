#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from core.handlers import CountdownHandler


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class WorkPageView(TemplateView):
    template_name = "work.html"


class CountdownView(TemplateView):
    template_name = "countdown.html"

    def get_context_data(self, **kwargs):
        context = super(CountdownView, self).get_context_data(**kwargs)
        return CountdownHandler.get_countdown_entries(context)

