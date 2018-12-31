from mongoengine.errors import DoesNotExist
from django.shortcuts import Http404
from django.views.generic.base import TemplateView, View
# Create your views here.
from blog.models import Post


class BlogListView(TemplateView):
    template_name = "blog/list.html"

    def get_context_data(self, **kwargs):
        ctx = super(BlogListView, self).get_context_data(**kwargs)
        from blog.migrations import publish_articles; publish_articles()
        ctx["posts"] = Post.objects.all()
        return ctx


class BlogDetailView(TemplateView):
    template_name = "blog/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(BlogDetailView, self).get_context_data(**kwargs)
        try:
            ctx["post"] = Post.objects.get(slug=kwargs.get('slug'))
        except DoesNotExist:
            Http404()
        return ctx

