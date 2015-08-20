# app specific urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse

import blog.views as blogviews

urlpatterns = patterns('',
    url(r'^blog/$', blogviews.BlogpageView.as_view(), name="blog_blogpage_view"),

)
