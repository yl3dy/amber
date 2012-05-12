from django.conf.urls.defaults import patterns, include, url
from views import mainpage, servers

urlpatterns = patterns('',
    url(r'^$', mainpage),
    url(r'^servers/$', servers),
    (r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'about.html'}),
    (r'^settings/$', 'django.views.generic.simple.direct_to_template', {'template': 'settings.html'}),
)
