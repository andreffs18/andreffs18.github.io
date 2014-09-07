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
from admin.models import BlogArticle
from core.settings import logger

class AdminBlogView(FormView):
    template_name = "admin/blog.html"
    form_class = BlogAddPostForm
    success_url = '?state=added'

    def get_context_data(self, **kwargs):
        context = super(AdminBlogView, self).get_context_data(**kwargs)
        context['articles'] = BlogArticle.objects.all()
        return context


    def form_valid(self, form):
        logger.debug("Form valid")
        BlogArticle.create_article(**form.cleaned_data)
        return super(AdminBlogView, self).form_valid(form)

class FeedsView(TemplateView):
    template_name = "admin/feeds.html"

    def get_context_data(self, **kwargs):
        context = super(FeedsView, self).get_context_data(**kwargs)
        return context

class AdminEditBlogArticleView(FormView):
    pass