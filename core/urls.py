from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import BlogView, ProjectsView, BlogDetailView, SignInView, ContactView

from core.settings import logger
logger.debug('''
========================================================================

        WELCOME TO MY PORTFOLIO DUMBASS! YOU SHOULDN'T BE HERE..

                            last update
                           04 - 09 - 2014

========================================================================
''')

urlpatterns = patterns('',


	url(r'^explore/$', TemplateView.as_view(template_name="home.html"), name='home'),

	url(r'^$', TemplateView.as_view(template_name="welcome.html"), name='welcome'),

	url(r'^blog/$', BlogView.as_view(), name='blog'),
    url(r'^blog/(?P<slug>[a-zA-Z0-9_/-]+)/$', BlogDetailView.as_view(), name="blog_detail"),

    url(r'^about/$', TemplateView.as_view(template_name="about/about.html"), name='about'),
	url(r'^work/$', TemplateView.as_view(template_name="work.html"), name='work'),
	url(r'^education/$', TemplateView.as_view(template_name="education/education.html"), name='education'),
	url(r'^projects/$', ProjectsView.as_view(), name='projects'),
	url(r'^contacts/$', ContactView.as_view(), name='contacts'),


	url(r'^admin/', include('admin.urls'), name="admin"),
    url(r'^signin/$','django.contrib.auth.views.login', name="sign_in"),
)
