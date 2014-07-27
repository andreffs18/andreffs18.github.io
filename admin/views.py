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

from admin.forms import BlogAddPostForm

class AdminBlogView(TemplateView, FormView):
    template_name = "admin/blog.html"
    form_class = BlogAddPostForm
    success_url = 'blog?state=added'

    def get_context_data(self, **kwargs):
        context = super(AdminBlogView, self).get_context_data(**kwargs)


        article = { "title" : "Something about something",
            "slug" : "12/08/2013/something-about-something/",
            "date" : "12 August 2013, 13h30",
            "body" : "I work swell, i sd jasldk njasoidkl jasdk asmdshad the luck to become a internshipjjjjjjjjjjjjjjjjjjjjjjjj on the first Portugues Startup to enter in YCombinator.. Unbabel! The just make a way for machine translation and a human have a baby and awesome text birth fromave a baby and awesome text birth fromave a baby and awesome text birth from it's windows",
            "comments" : "12",
            "time" : "3",
            "categories" : ["aha", "beads", "hasd", "ajsd"]
        }

        entries = []
        for i in range(10):
            entries.append(article)

        context['articles'] = entries
        return context


    def form_valid(self, form):
        #form.send_email()
        return super(AdminBlogView, self).form_valid(form)