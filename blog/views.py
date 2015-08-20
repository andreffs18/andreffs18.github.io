from django.shortcuts import render
from django.views.generic.base import TemplateView, View
# Create your views here.


class BlogpageView(TemplateView):
    template_name = "blog/blog.html"

    def get_context_data(self, **kwargs):
        ctx = super(BlogpageView, self).get_context_data(**kwargs)
        return ctx
