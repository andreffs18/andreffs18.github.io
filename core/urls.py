from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',

    
    url(r'explore/^$', TemplateView.as_view(template_name="home.html"), name='home'),

	url(r'^$', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about'),
    
    url(r'^blog/$', TemplateView.as_view(template_name="blog.html"), name='blog'),
    url(r'^social/$', TemplateView.as_view(template_name="social.html"), name='social'),

    # url(r'^blog/', include('blog.urls')),
    
    #url(r'^admin/', include(admin.site.urls)),
)
