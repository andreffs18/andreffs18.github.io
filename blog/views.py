from django.shortcuts import render
from django.views.generic.base import TemplateView, View
# Create your views here.

import blog.services as blogservices
import blog.models as blogmodels


class BlogListView(TemplateView):
    template_name = "blog/list.html"

    def get_context_data(self, **kwargs):
        ctx = super(BlogListView, self).get_context_data(**kwargs)

        articles = blogmodels.Articles.all()
        ctx["articles"] = list(articles)

        return ctx


class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(BlogDetailView, self).get_context_data(**kwargs)

        article = blogmodels.Articles.filter(**{'slug': kwargs.get('slug')})
        ctx["article"] = article

        return ctx
