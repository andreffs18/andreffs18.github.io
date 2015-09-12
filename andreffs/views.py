#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView, View
import andreffs.utils as affsutils
import json

class HomepageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super(HomepageView, self).get_context_data(**kwargs)
        ctx['cv'] = affsutils.generate_cv()
        return ctx


class AboutpageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        ctx = super(AboutpageView, self).get_context_data(**kwargs)
        ctx['about'] = affsutils.generate_about()
        return ctx


class WorkpageView(TemplateView):
    template_name = "work.html"

    def get_context_data(self, **kwargs):
        ctx = super(WorkpageView, self).get_context_data(**kwargs)
        return ctx