# project wide urls
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


import views as v


urlpatterns = patterns('',
    url(r'^$', v.HomePageView.as_view(), name="home"),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout',
        kwargs={'next_page': '/'}),
    # url(r'^', include('django.contrib.auth.urls')),

    url(r'^about/$', v.AboutPageView.as_view(), name="about"),
    url(r'^work/$', v.WorkPageView.as_view(), name="work"),
    url(r'^blog/', include('blog.urls', namespace="blog")),

    url(r'^countdown/$', v.CountdownView.as_view(), name="countdown"),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()
# if not settings.DEBUG:
#     urlpatterns += patterns('',
#         (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#          {'document_root': settings.STATIC_ROOT}),
#     )
