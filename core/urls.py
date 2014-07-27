from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from core.views import BlogView, ProjectsView, BlogDetailView
import logging


admin.autodiscover()


logger = logging.getLogger()
logger.debug("LoL")

urlpatterns = patterns('',


	url(r'^explore/$', TemplateView.as_view(template_name="home.html"), name='home'),

	url(r'^$', TemplateView.as_view(template_name="welcome.html"), name='welcome'),
	url(r'^about/$', TemplateView.as_view(template_name="about/about.html"), name='about'),
	url(r'^blog/$', BlogView.as_view(), name='blog'),

	url(r'^blog/12/08/2013/something-about-something/$', BlogDetailView.as_view(), name="blogdetail"),


	url(r'^work/$', TemplateView.as_view(template_name="work.html"), name='work'),
	url(r'^college/$', TemplateView.as_view(template_name="college.html"), name='college'),
	url(r'^projects/$', ProjectsView.as_view(), name='projects'),


	url(r'^contacts/$', TemplateView.as_view(template_name="contacts/contacts.html"), name='contacts'),


	url(r'^admin/', include('admin.urls'), name="admin"),

    # url(r'^blog/', ),
    
    #url(r'^admin/', include(admin.site.urls)),
)
