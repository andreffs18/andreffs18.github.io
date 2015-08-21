# project wide urls
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView, View
from django.core.urlresolvers import reverse
from django.contrib import admin

admin.autodiscover()

import andreffs.views as coreviews

# import your urls from each app here, as needed
urlpatterns = patterns('',

    url(r'^$', coreviews.HomepageView.as_view(), name="core_homepage_view"),
    url(r'^about/$', coreviews.AboutpageView.as_view(), name="core_aboutpage_view"),
    url(r'^work/$', coreviews.WorkpageView.as_view(), name="core_workpage_view"),
    url(r'', include('blog.urls')),


    # urls specific to this app

    # url(r'^/$', TemplateView.as_view(template_name="home.html"), name="core_home_view"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #
    # url(r'^admin/', include(admin.site.urls)),

    # catch all, redirect to core home view
    # url(r'', RedirectView.as_view(url='/core/home')),
)
