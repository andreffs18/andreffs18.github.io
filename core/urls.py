# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

import core.views as coreviews

urlpatterns = patterns('',
    url(r'^$', coreviews.HomepageView.as_view(), name="core_homepage_view"),
    url(r'^about/$', coreviews.AboutpageView.as_view(), name="core_aboutpage_view"),
    url(r'^work/$', coreviews.WorkpageView.as_view(), name="core_workpage_view"),
)
