#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
André Silva 1st April 2014  
'''

import logging
import json
from django.template.loader import get_template
from django.template.context import Context

from django.views.generic.base import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

logger = logging.getLogger('andreffs.' + __name__)

class BlogView(TemplateView):
	template_name = "blog.html"

	def get_context_data(self, **kwargs):
		context = super(BlogView, self).get_context_data(**kwargs)

		context["test"] = "test"

		return context

class ProjectsView(TemplateView):
	template_name = "projects.html"

	def get_context_data(self, **kwargs):
		context = super(ProjectsView, self).get_context_data(**kwargs)

		projects = []
		for i in range(20):
			projects.append({ "img" : "../static/img/workshowreel/img%s.jpg" % ((i%3) +1), "title": "Title %s" % (i), "subtitle": "asnd kja hls dk"})

		context["projects"] = projects
		
		return context
