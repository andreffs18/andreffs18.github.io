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
from core.settings import logger

from admin.models import BlogArticle

from core.forms import ContactForm

class BlogView(TemplateView):
	template_name = "blog/blog.html"

	def get_context_data(self, **kwargs):
		context = super(BlogView, self).get_context_data(**kwargs)

		articles = BlogArticle.objects.all().order_by('-date')

		paginator = Paginator(articles, 5)
		page = self.request.GET.get('page')
		try:
			order_list = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			order_list = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			order_list = paginator.page(paginator.num_pages)

		context["articles"] =  order_list
		return context


class BlogDetailView(TemplateView):
	template_name = "blog/blog-detail.html"

	def get_context_data(self, **kwargs):
		context = super(BlogDetailView, self).get_context_data(**kwargs)

		article = BlogArticle.objects.get(slug=kwargs['slug'])

		context["article"] = article
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

class SignInView():
    pass

class ContactView(FormView):
    template_name = "contacts/contacts.html"
    form_class = ContactForm
    success_url = '?state=added'