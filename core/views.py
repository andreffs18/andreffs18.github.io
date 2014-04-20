#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
André Silva 1st April 2014  
'''

import logging
import json
from django.template.loader import get_template
from django.template.context import Context

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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


		article = { "title" : "Something about something", 
					"date" : "12 August 2013, 13h30",
					"body" : "I work swell, i had the luck to become a internship on the first Portugues Startup to enter in YCombinator.. Unbabel! The just make a way for machine translation and a human have a baby and awesome text birth from it's windows",
					"comments" : "12",
					"categories" : ["aha", "beads", "hasd", "ajsd"] 
					} 

		entries = []
		for i in range(10):
			entries.append(article)

		context["tags"] = ["aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "aha", "beads", "hasd", "ajsd"]
		context["recent_posts"] = [" asdljksa dlksja dlskasdasdasdas ds ds adajd lsakj daslkjd ossidasdsae", "somthing nice to say to ppl", "hellow owrlds"]

		paginator = Paginator(entries, 2)
		page = self.request.GET.get('page')
		try:
			order_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			order_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			order_list = paginator.page(paginator.num_pages)

		context["entries"] =  order_list
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
