# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

import blog.views as blogviews

urlpatterns = patterns('',
    url(r'^$', blogviews.BlogPageView.as_view(), name="blog_view"),
    url(r'^(?P<slug>[\w-]+)/$', blogviews.BlogDetailView.as_view(), name="blog_detail_view"),
)
