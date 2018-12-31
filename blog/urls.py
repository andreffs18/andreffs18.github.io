# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

from blog.views import BlogDetailView, BlogListView

urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name="list"),
    url(r'^(?P<slug>[\w-]+)/$', BlogDetailView.as_view(), name="detail"),
)
