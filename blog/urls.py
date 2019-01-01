# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

from blog.views import BlogDetailView, BlogListView

urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name="list"),
    url(r'^(?P<page>[\d]{1,2})$', BlogListView.as_view(), name="list"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<title>.*)$',
        BlogDetailView.as_view(), name="detail"),
)
