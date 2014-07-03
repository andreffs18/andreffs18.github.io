from django.conf.urls import patterns, include, url
from blog.views import BlogView, BlogDetailView


urlpatterns = patterns('',

    url(r'^$', BlogView.as_view(), name='blog'),
    url(r'^blog/12/08/2013/something-about-something/$', BlogDetailView.as_view(), name="blogdetail"),

    #http://www.chrisumbel.com/article/django_python_mongodb_engine_mongo
    #http://expresso.sapo.pt/licoes-de-vida-que-vai-aprender-ate-aos-30=f864581
)
