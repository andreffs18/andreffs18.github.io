from django.conf.urls import patterns, url

from blog.views.blog_list_view import  BlogListView
from blog.views.blog_detail_view import BlogDetailView


urlpatterns = patterns('',
    url(r'^$', BlogListView.as_view(), name="list"),
    url(r'^(?P<page>[\d]{1,2})$', BlogListView.as_view(), name="list"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<title>.*)$',
        BlogDetailView.as_view(), name="detail"),
)
