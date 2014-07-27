from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from admin.views import AdminBlogView


urlpatterns = patterns('',



    url(r'^$', TemplateView.as_view(template_name="admin/homepage.html"), name='admin_homepage'),
    url(r'^blog/$', AdminBlogView.as_view(), name='admin_blog'),

)
