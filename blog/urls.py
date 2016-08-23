# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

import views as v

urlpatterns = patterns('',
    url(r'^$', v.BlogListView.as_view(), name="list"),
    url(r'^(?P<slug>[\w-]+)/$', v.BlogDetailView.as_view(), name="detail"),
)
