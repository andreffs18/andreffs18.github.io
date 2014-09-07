from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from admin.views import AdminBlogView, AdminEditBlogArticleView, FeedsView
from admin.models import delete_blog_article


urlpatterns = patterns('',



    url(r'^$', TemplateView.as_view(template_name="admin/homepage.html"), name='admin_homepage'),
    url(r'^blog/$', AdminBlogView.as_view(), name='admin_blog'),
    url(r'^feeds/$', FeedsView.as_view(), name='admin_feeds'),

    url(r'^blog/delete/$', delete_blog_article, name='admin_blog'),
    url(r'^blog/edit/$', AdminEditBlogArticleView.as_view(), name='admin_blog'),
)
